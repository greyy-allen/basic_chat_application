from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from .db import (
    rooms_collection,
    users_collection,
    room_members_collection,
    messages_collection,
)
from bson.objectid import ObjectId
from pymongo import DESCENDING


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def is_authenticated(self):
        return True

    @staticmethod
    def is_active(self):
        return True

    @staticmethod
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def check_password(self, password_input):
        return check_password_hash(self.password, password_input)

    @staticmethod
    def save_user(username, email, password):
        password_hash = generate_password_hash(password)
        users_collection.insert_one(
            {"_id": username, "email": email, "password": password_hash}
        )

    @staticmethod
    def get_user(username):
        user_data = users_collection.find_one({"_id": username})
        return (
            User(user_data["_id"], user_data["email"], user_data["password"])
            if user_data
            else None
        )


class Room:
    def __init__(self, room_id, room_name):
        self.room_id = room_id
        self.room_nmae = room_name

    @staticmethod
    def save_room(room_name, created_by):
        room_id = rooms_collection.insert_one(
            {
                "name": room_name,
                "created_by": created_by,
                "created_at": datetime.now(),
            }
        ).inserted_id
        Room.add_room_member(
            room_id, room_name, created_by, created_by, is_room_admin=True
        )
        return room_id

    @staticmethod
    def get_room(room_id):
        return rooms_collection.find_one({"_id": ObjectId(room_id)})

    @staticmethod
    def update_room(room_id, room_name):
        rooms_collection.update_one(
            {"_id": ObjectId(room_id)}, {"$set": {"name": room_name}}
        )
        room_members_collection.update_many(
            {"_id.room_id": ObjectId(room_id)}, {"$set": {"room_name": room_name}}
        )

    @staticmethod
    def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
        room_members_collection.insert_one(
            {
                "_id": {"room_id": ObjectId(room_id), "username": username},
                "room_name": room_name,
                "added_by": added_by,
                "added_at": datetime.now(),
                "is_room_admin": is_room_admin,
            }
        )

    @staticmethod
    def add_room_members(room_id, room_name, usernames, added_by):
        room_members_collection.insert_many(
            [
                {
                    "_id": {"room_id": ObjectId(room_id), "username": username},
                    "room_name": room_name,
                    "added_by": added_by,
                    "added_at": datetime.now(),
                    "is_room_admin": False,
                }
                for username in usernames
            ]
        )

    @staticmethod
    def get_room_members(room_id):
        return list(room_members_collection.find({"_id.room_id": ObjectId(room_id)}))

    @staticmethod
    def get_rooms_for_user(username):
        return list(room_members_collection.find({"_id.username": username}))

    @staticmethod
    def remove_room_members(room_id, usernames):
        room_members_collection.delete_many(
            {
                "_id": {
                    "$in": [
                        {"room_id": ObjectId(room_id), "username": username}
                        for username in usernames
                    ]
                }
            }
        )

    @staticmethod
    def is_room_member(room_id, username):
        return (
            room_members_collection.count_documents(
                {"_id": {"room_id": ObjectId(room_id), "username": username}}
            )
            > 0
        )

    @staticmethod
    def is_room_admin(room_id, username):
        return (
            room_members_collection.count_documents(
                {
                    "_id": {"room_id": ObjectId(room_id), "username": username},
                    "is_room_admin": True,
                }
            )
            > 0
        )


MESSAGE_FETCH_LIMIT = 3


class Message:
    def __init__(self, message_id, text, sender, room_id):
        self.message_id = message_id
        self.text = text
        self.sender = sender
        self.room_id = room_id

    @staticmethod
    def save_message(room_id, text, sender):
        messages_collection.insert_one(
            {
                "room_id": ObjectId(room_id),
                "text": text,
                "sender": sender,
                "created_at": datetime.now(),
            }
        )

    @staticmethod
    def get_messages(room_id, page=0):
        offset = page * MESSAGE_FETCH_LIMIT
        messages = list(
            messages_collection.find({"room_id": ObjectId(room_id)})
            .sort("_id", DESCENDING)
            .limit(MESSAGE_FETCH_LIMIT)
            .skip(offset)
        )
        for message in messages:
            message["created_at"] = message["created_at"].strftime("%d %b, %H:%M")
        return messages[::-1]

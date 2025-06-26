from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from .db import rooms_collection, users_collection, room_members_collection
from bson.objectid import ObjectId


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
                "room_name": room_name,
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
        rooms_collection.find_one({"_id": ObjectId(room_id)})

    @staticmethod
    def add_room_member(room_id, room_name, username, added_by, is_room_admin=False):
        room_members_collection.insert_one(
            {
                "_id": {"room_id": room_id, "username": username},
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
                    "_id": {"room_id": room_id, "username": username},
                    "room_name": room_name,
                    "added_by": added_by,
                    "added_at": datetime.now(),
                    "is_room_admin": False,
                }
                for username in usernames
            ]
        )

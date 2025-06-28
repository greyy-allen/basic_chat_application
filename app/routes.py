from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Room

main = Blueprint("main", __name__)


@main.route("/")
def home():
    rooms = []
    if current_user.is_authenticated:
        rooms = Room.get_rooms_for_user(current_user.username)
    return render_template("index.html", rooms=rooms)


@main.route("/rooms/<room_id>")
@login_required
def view_room(room_id):
    room = Room.get_room(room_id)
    print(room)
    if room and Room.is_room_member(room_id, current_user.username):
        room_members = Room.get_room_members(room_id)
        return render_template(
            "view_room.html",
            room=room,
            username=current_user.username,
            room_members=room_members,
        )
    else:
        return "Room not found", 404


@main.route("/create-room", methods=["GET", "POST"])
@login_required
def create_room():
    message = ""
    if request.method == "POST":
        room_name = request.form.get("room_name")
        usernames = [
            username.strip() for username in request.form.get("members").split(",")
        ]

        if len(room_name) and len(usernames):
            room_id = Room.save_room(room_name, current_user.username)

            if current_user.username in usernames:
                usernames.remove(current_user.username)
            Room.add_room_members(room_id, room_name, usernames, current_user.username)
            return redirect(url_for("view_room", room_id))
        else:
            message = "Failed to create room"
    return render_template("create_room.html", message=message)


@main.route("/rooms/<room_id>/edit", methods=["GET", "POST"])
@login_required
def edit_room(room_id):
    room = Room.get_room(room_id)
    if room and Room.is_room_admin(room_id, current_user.username):
        existing_room_members = [
            member["_id"]["username"] for member in Room.get_room_members(room_id)
        ]
        room_members_str = ",".join(existing_room_members)
        message = ""
        if request.method == "POST":
            room_name = request.form.get("room_name")
            room["name"] = room_name
            Room.update_room(room_id, room_name)

            new_members = [
                username.strip() for username in request.form.get("members").split(",")
            ]
            members_to_add = list(set(new_members) - set(existing_room_members))
            members_to_remove = list(set(existing_room_members) - set(new_members))
            if len(members_to_add):
                Room.add_room_members(
                    room_id, room_name, members_to_add, current_user.username
                )
            if len(members_to_remove):
                Room.remove_room_members(room_id, members_to_remove)
            message = "Room edited successfully"
            room_members_str = ",".join(new_members)

        return render_template(
            "edit_room.html",
            room=room,
            room_members_str=room_members_str,
            message=message,
        )
    else:
        return "Room not found", 404

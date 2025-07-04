from flask_socketio import join_room, leave_room
from datetime import datetime
from .models import Message


def register_socket_handlers(socketio, app):
    @socketio.on("join_room")
    def handle_join_room_event(data):
        app.logger.info(
            "{} has joined the room {}".format(data["username"], data["room"])
        )
        join_room(data["room"])
        socketio.emit("join_room_announcement", data)

    @socketio.on("send_message")
    def handle_send_message_event(data):
        app.logger.info(
            "{} has sent message to the room {}: {}".format(
                data["username"], data["room"], data["message"]
            )
        )
        data["created_at"] = datetime.now().strftime("%d %b, %H:%M")
        Message.save_message(data["room"], data["message"], data["username"])
        socketio.emit("receive_message", data, room=data["room"])

    @socketio.on("leave_room")
    def handle_leave_room_event(data):
        app.logger.info(
            "{} has left the room {}".format(data["username"], data["room"])
        )
        leave_room(data["room"])
        socketio.emit("leave_room_announcement", data, room=data["room"])

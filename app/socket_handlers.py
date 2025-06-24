from flask_socketio import join_room

def register_socket_handlers(socketio, app):
  @socketio.on('join_room')
  def handle_join_room_event(data):
      app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
      join_room(data['room'])
      socketio.emit('join_room_announcement', data)

  @socketio.on('send_message')
  def handle_send_message_event(data):
      app.logger.info("{} has sent message to the room {}: {}".format(data['username'], 
                                                                      data['room'],
                                                                      data['message']))
      socketio.emit('receive_message', data, room=data['room'])

from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    socketio.init_app(app)

    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .socket_handlers import register_socket_handlers
    register_socket_handlers(socketio, app)

    return app
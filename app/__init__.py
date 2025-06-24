from flask import Flask
from flask_socketio import SocketIO
from flask_login import LoginManager

socketio = SocketIO()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = 'thisisasecretkey'

  socketio.init_app(app)
  login_manager.init_app(app)

  from .models import User

  @login_manager.user_loader
  def load_user(username):
    return User.get_user(username)


  from .routes import main as main_blueprint
  app.register_blueprint(main_blueprint)

  from .socket_handlers import register_socket_handlers
  register_socket_handlers(socketio, app)

  from .auth import auth as auth_blueprint
  app.register_blueprint(auth_blueprint)

  login_manager.login_view = 'auth.login'

  return app
from werkzeug.security import check_password_hash

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
    from werkzeug.security import generate_password_hash
    from .db import users_collection
    password_hash = generate_password_hash(password)
    users_collection.insert_one({'_id': username, 'email': email, 'password': password_hash})

  @staticmethod
  def get_user(username):
    from .db import users_collection
    user_data = users_collection.find_one({'_id': username})
    return User(user_data['_id'], user_data['email'], user_data['password']) if user_data else None
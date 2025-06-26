from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from pymongo.errors import DuplicateKeyError
from .models import User
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

  if current_user.is_authenticated:
        return redirect(url_for('main.home'))
  
  message = ''
  if request.method == 'POST':
    username = request.form.get('username')
    password_input = request.form.get('password')
    user = User.get_user(username)

    if user and user.check_password(password_input):
      login_user(user)
      return redirect(url_for('main.home'))
    else:
      message = 'Failed to login!'

  return render_template('login.html', message = message)

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('main.home'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

  if current_user.is_authenticated:
        return redirect(url_for('main.home'))

  message = ''
  if request.method == 'POST':
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    try:
      User.save_user(username, email, password)
      return redirect(url_for('auth.login'))
    except DuplicateKeyError:
      message = "User already exists!"
  return render_template('signup.html', message = message)
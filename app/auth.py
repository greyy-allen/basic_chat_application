from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
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
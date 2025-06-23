from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
  return render_template("index.html")

def chat():
  username = request.args.get('username')
  room = request.args.get('room')

  if username and room:
    return render_template('chat.html', username=username, room=room)
  else:
    return redirect(url_for('main.home'))
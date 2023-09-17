from flask import Flask, render_template
from authentication import authentication
from chat import chat
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, join_room, leave_room

from database import get_user, save_message

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret"
login_manager = LoginManager(app)
socketio = SocketIO(app)

app.register_blueprint(authentication)
app.register_blueprint(chat)


# flask_login injection
@login_manager.user_loader
def load_user(username):
    return get_user(username)


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template(
            template_name_or_list="index.html",
            logged_in=current_user.is_authenticated,
            current_user=current_user
        )
    return render_template(template_name_or_list="index.html")


# SocketIO Events and Emits
@socketio.on("join_room")
def handle_join_room_event(data):
    """Handle the join room event from socket.on() in js"""
    app.logger.info(f"{data['username']} has joined the room {data['room_id']}")
    join_room(data["room_id"])
    socketio.emit("join_room_announcement", data)  # we should handle this event in javascript


@socketio.on("send_message")
def handle_send_message_event(data):
    """Handle the send message event from socket.on() in javascript """
    app.logger.info(f"{data['username']} has sent a message to the room {data['room_id']}: {data['message']}")
    save_message(room_id=data['room_id'], text=data['message'], sender=data['username'])
    socketio.emit("receive_message", data, room=data["room_id"])
    # from backend to frontend, we should handle this event in javascript.


@socketio.on("leave_room")
def handle_leave_room_event(data):
    app.logger.info(f"{data['username']} has left the room {data['room_id']}")
    leave_room(data['room_id'])
    socketio.emit('leave_room_announcement', data, room=data['room_id'])


if __name__ == '__main__':
    socketio.run(app, debug=True)

import os
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, join_room, leave_room
from dotenv import load_dotenv
from authentication import authentication
from chat import chat
from dashboard import dashboard_operations
from database import get_user, save_message, fetch_latest_message

load_dotenv("./.env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRETKEY")
login_manager = LoginManager(app)
socketio = SocketIO(app)

# blue prints
app.register_blueprint(authentication)
app.register_blueprint(chat)
app.register_blueprint(dashboard_operations)

# Enviorment functions
app.jinja_env.filters['fetch_latest_message'] = fetch_latest_message


# flask_login injection
@login_manager.user_loader
def load_user(username):
    return get_user(username)


@app.route(rule='/')
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
def handle_join_room_event(data) -> None:
    """
    Handle the join room event from socket.on() in javascript.

    :param data: JSON data parsed from javascript.
    :return: None
    """
    app.logger.info(f"{data['username']} has joined the room {data['room_id']}")
    join_room(data["room_id"])
    socketio.emit("join_room_announcement", data)  # we should handle this event in javascript


@socketio.on("send_message")
def handle_send_message_event(data) -> None:
    """
    Handle the sent message event from socket.on() in javascript.

    :param data: JSON data parsed from javascript.
    :return: None
    """
    app.logger.info(f"{data['username']} has sent a message to the room {data['room_id']}: {data['message']}")
    save_message(room_id=data['room_id'], text=data['message'], sender=data['username'])
    socketio.emit("receive_message", data, room=data["room_id"])
    # from backend to frontend, we should handle this event in javascript.


@socketio.on("leave_room")
def handle_leave_room_event(data) -> None:
    """
    Handle leave room event from socket.on() in javascript.
    :param data: JSON data parsed from javascript.
    :return: None
    """
    app.logger.info(f"{data['username']} has left the room {data['room_id']}")
    leave_room(data['room_id'])
    socketio.emit('leave_room_announcement', data, room=data['room_id'])


if __name__ == '__main__':
    socketio.run(app, debug=True)

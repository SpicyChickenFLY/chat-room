"""socketio事件处理"""

from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio

@socketio.on('join', namespace='/chat')
def joined(_):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {
        'msg': f"{session.get('name')} has entered the room.",
    }, to=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {
        'msg': f"{session.get('name')}: {message['msg']}",
    }, to=room)

# 发送消息
@socketio.on("sendMsg")
def handle_send_message(data):
    # 存储信息

    # 广播消息
    socketio.send({"type": "msg", "data": data})


@socketio.on('leave', namespace='/chat')
def left(_):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {
        'msg': f"{session.get('name')} has left the room.",
    }, to=room)

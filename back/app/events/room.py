"""socketio事件处理"""

from flask import session
from flask_socketio import emit, join_room, leave_room

from . import socketio

from app import services

@socketio.on("join", namespace="/chat")
def joined(_):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    join_room(room)
    emit(
        "status",
        {
            "msg": f"{session.get('name')} has entered the room.",
        },
        to=room,
    )


@socketio.on("text", namespace="/chat")
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get("room")
    emit(
        "message",
        {
            "msg": f"{session.get('name')}: {message['msg']}",
        },
        to=room,
    )


# 发送消息
@socketio.on("msg")
def handle_send_message(data, what):
    print(what)
    # 存储信息
    user_id = data["userId"]
    room_id = data["roomId"]
    content = data["content"]
    chat = services.create_chat(room_id, user_id, content)
    # 广播消息
    resp_data = {
        "userId": chat.user_id,
        "roomId": chat.room_id,
        "content": chat.content,
    }
    socketio.emit("msg", {"type": "msg", "data": resp_data})


@socketio.on("leave", namespace="/chat")
def left(_):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get("room")
    leave_room(room)
    emit(
        "status",
        {
            "msg": f"{session.get('name')} has left the room.",
        },
        to=room,
    )

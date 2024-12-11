from flask_socketio import SocketIO

socketio = None

def init_socket(app):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins="*")

    from . import room
    # socketio.on_event("connect", room.on_connect)
    # socketio.on_event("disconnect", room.on_disconnect)
    # socketio.on_event("message", room.on_message)


def run_socket(app):
    socketio.run(app, host="0.0.0.0", port=5000)

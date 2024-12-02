from sqlalchemy.sql import func, case

from app.entities import *
from app.store import db


# def list_room():
#     return Room.query.all()
#
#
# def get_room(id: str):
#     return db.session.get(Room, id)
#
#
# def find_room_by_name(room_name: str):
#     return Room.query.filter_by(name=room_name).one()
#
#
# def create_room(room: Room):
#     db.session.add(room)
#     db.session.commit()
#     return room
#

def get_chat_for_room(room_id: int, last_chat_id: int, limit: int = 50):
    return (
        Chat.query
        .filter(Chat.room_id == room_id)
        .filter(Chat.id < last_chat_id)
        .order_by(Chat.id.desc())
        .limit(limit)
    ).all()

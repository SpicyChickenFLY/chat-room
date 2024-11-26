from app.entities import Room
from app.store import db


def list_room():
    return Room.query.all()

def get_room(id: str):
    return db.session.get(Room, id)

def find_room_by_name(room_name: str):
    return Room.query.filter_by(name=room_name).one()


def create_room(room: Room):
    db.session.add(room)
    db.session.commit()
    return room

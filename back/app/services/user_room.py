from app.entities import UserRoom
from app.store import db

def list_user_room(user_id: None|str, room_id: None|str):
    return UserRoom.query.filter_by(user_id=user_id, room_id=room_id).all()

def get_user_room(user_id: str, room_id: str):
    return UserRoom.query.get({"user_id": user_id, "room_id":room_id})

def create_user_room(user_room):
    db.session.add(user_room)
    db.session.commit()
    return user_room

from app.entities import *
from app.store import db


def list_user():
    return User.query.all()

def get_user(id: str):
    return User.query.get(id)

def find_user_by_nickname(nickname: str):
    return User.query.filter_by(nickname=nickname).first()


def create_user(user: User):
    db.session.add(user)
    db.session.commit()
    return user

def get_user_details_for_room(room_id: int):
    return (
        db.session.query(
            UserRoomMap.user_id.label("id"),
            User.nickname.label("nickname"),
            User.avatar.label("avatar"),
        )
        .outerjoin(User, User.id == UserRoomMap.user_id)
        .filter(UserRoomMap.room_id == room_id)
    ).all()

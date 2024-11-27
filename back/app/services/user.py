from app.entities import User
from app.store import db


def list_user():
    return User.query.all()

def get_user(id: str):
    return db.session.get(User, id)

def find_user_by_nickname(nickname: str):
    return User.query.filter_by(nickname=nickname).first()


def create_user(user: User):
    db.session.add(user)
    db.session.commit()
    return user

from app.entities import User
from app.store import sql_session


def list_users():
    return sql_session.query(User).all()


def find_user_by_nickname(nickname: str):
    return sql_session.query(User).filter_by(nickname=nickname).one()


def create_user(user: User):
    sql_session.add(user)
    sql_session.commit()
    return sql_session.query(User).filter_by(nickname=user.nickname).one()

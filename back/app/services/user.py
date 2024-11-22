from app.entities import User
from app.store import sql_session


def list_user():
    return sql_session.query(User).all()

def get_user(id: str):
    return sql_session.query(User).get(id)

def find_user_by_nickname(nickname: str):
    return sql_session.query(User).filter_by(nickname=nickname).one()


def create_user(user: User):
    sql_session.add(user)
    sql_session.commit()
    return sql_session.query(User).filter_by(nickname=user.nickname).one()

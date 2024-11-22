from app.entities import UserRoom, User, Room
from app.store import sql_session

def list_user_room(user_id: str, room_id: str):
    return sql_session.query(UserRoom).filter_by(user_id=user_id, room_id=room_id).all()

def get_user_room(user_id: str, room_id: str):
    return sql_session.query(UserRoom).get((user_id, room_id))

def create_user_room(user: User):
    sql_session.add(user)
    sql_session.commit()
    return sql_session.query(User).filter_by(nickname=user.nickname).one()

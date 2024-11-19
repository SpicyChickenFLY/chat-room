from sqlalchemy import sql
from back.app.entities.user import User
from . import sql_session

def list_users():
    user = sql_session.query(User).all()
    return user

def find_user():
    user = sql_session.query(User).filter_by(user_name="").first()
    return user

def create_user(user: User):
    sql_session.add(user)
    sql_session.commit()

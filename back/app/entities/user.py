import datetime

from app.store import db


class User(db.Model):
    __tablename__ = "user_list"

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String, unique=True)
    token = db.Column(db.String)
    avatar = db.Column(db.String, default="avatar_default.png")
    status = db.Column(db.SmallInteger, default=0)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

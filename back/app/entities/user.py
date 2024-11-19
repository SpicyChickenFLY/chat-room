import datetime

from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user_list"

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    token = Column(String)
    avatar = Column(String, default="avatar_default.png")
    status = Column(SmallInteger, default=0)
    create_time = Column(DateTime, default=datetime.datetime.now())

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.nickname,
            "avatar": self.avatar,
            "status": self.status
        }

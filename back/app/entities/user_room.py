from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import declarative_base


class UserRoom(declarative_base()):
    __tablename__ = "user_room_map"

    room_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)
    authority = Column(Integer)
    mute = Column(Integer)

    def to_dict(self):
        return {
            "userId": self.user_id,
            "userName": self.user_name,
            "userImg": self.user_img,
        }

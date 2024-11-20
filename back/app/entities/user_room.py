from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import declarative_base


class UserRoom(declarative_base()):
    __tablename__ = "user_room_map"

    user_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, primary_key=True)
    authority = Column(Integer)
    mute = Column(Integer)
    create_time = Column(DateTime)

    def to_dict(self):
        return {
            "userId": self.user_id,
            "roomId": self.user_id,
            "authority": self.authority,
            "mute": self.mute
        }

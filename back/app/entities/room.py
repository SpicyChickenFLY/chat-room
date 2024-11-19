from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import declarative_base


class Room(declarative_base()):
    __tablename__ = "room_list"

    room_id = Column(Integer, primary_key=True)
    room_name = Column(String)
    room_img = Column(String)
    create_time = Column(DateTime)

    def to_dict(self):
        return {
            "roomId": self.room_id,
            "roomName": self.room_name,
            "roomImg": self.room_img,
        }

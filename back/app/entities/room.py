from sqlalchemy import Column, Integer, String, SmallInteger, DateTime
from sqlalchemy.orm import declarative_base


class Room(declarative_base()):
    __tablename__ = "room_list"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    avatar = Column(String)
    create_time = Column(DateTime)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "avatar": self.avatar,
        }

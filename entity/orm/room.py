from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Room(Base):
    """用户信息表"""
    __tablename__ = "room"

    id = Column(String, primary_key=True)
    name = Column(String)

    def to_dict(self):
        """返回JSON格式"""
        return {
            "id": self.id,
            "name": self.name,
        }

from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """用户信息表"""
    __tablename__ = "user"

    id = Column(String, primary_key=True)
    token = Column(String)
    account = Column(String)
    password = Column(String)
    nick = Column(String)
    avatar = Column(String)
    status = Column(SmallInteger)

    def to_dict(self):
        """返回JSON格式"""
        return {
            "id": self.id,
            "token": self.token,
            "account": self.account,
            "nick": self.nick,
            "avatar": self.avatar,
        }

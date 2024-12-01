from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from app.entities import *
from app.store import db


def list_room():
    return Room.query.all()


def get_room(id: str):
    return db.session.get(Room, id)


def find_room_by_name(room_name: str):
    return Room.query.filter_by(name=room_name).one()


def create_room(room: Room):
    db.session.add(room)
    db.session.commit()
    return room


def get_room_details_for_user(user_id: int):
    #1 Subquery to find the latest chat for each room
    latest_chat_subquery = (
        db.session.query(
            Chat.room_id,
            func.max(Chat.id).label('latest_chat_id'),
            Chat.content.label('latest_chat_content')
        )
        .group_by(Chat.room_id)
    ).subquery()

    # 2. 连接 user_room_map, room, chat 以及最新消息子查询
    query = (
        db.session.query(
            UserRoomMap.room_id,
            Room.name.label('room_name'),
            func.count(Chat.id).label('unread_messages'),
            latest_chat_subquery.c.latest_chat_content
        )
        .join(Room, Room.id == UserRoomMap.room_id)
        .outerjoin(Chat, Chat.room_id == UserRoomMap.room_id)
        .outerjoin(latest_chat_subquery, latest_chat_subquery.c.room_id == UserRoomMap.room_id)
        .filter(UserRoomMap.user_id == user_id)
        .filter((Chat.id > UserRoomMap.last_confirm_chat_id) | (UserRoomMap.last_confirm_chat_id == None))
        .group_by(UserRoomMap.room_id, Room.name, latest_chat_subquery.c.latest_chat_id, latest_chat_subquery.c.latest_chat_content)
    ).all()

    return query

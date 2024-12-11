from sqlalchemy.orm import aliased
from sqlalchemy.sql import func, case, label, outerjoin

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
    # Step 1: 子查询 - 获取用户的所有房间
    room_list = (
        db.session.query(
            UserRoomMap.room_id.label("room_id"),
            Room.name.label("room_name"),
            UserRoomMap.last_confirm_chat_id.label("last_confirm_chat_id"),
        )
        .outerjoin(Room, (UserRoomMap.room_id == Room.id))
        .filter(UserRoomMap.user_id == user_id)
    ).subquery()

    # Step 2: 子查询 - 获取每个房间的未读消息数量
    new_msg_count = (
        db.session.query(
            room_list.c.room_id.label("room_id"),
            func.count(Chat.id).label("new_msg_count"),
        )
        .outerjoin(
            Chat,
            (room_list.c.room_id == Chat.room_id)
            & (
                case(
                    (
                        room_list.c.last_confirm_chat_id.isnot(None),
                        room_list.c.last_confirm_chat_id,
                    ),
                    else_=0,
                )
                < Chat.id
            ),
        )
        .group_by(room_list.c.room_id)
    ).subquery()

    latest_chat_id = (
        db.session.query(
            room_list.c.room_id.label("room_id"),
            func.max(Chat.id).label("latest_chat_id"),
        )
        .outerjoin(Chat, (room_list.c.room_id == Chat.room_id))
        .group_by(room_list.c.room_id)
    ).subquery()

    latest_chat = (
        db.session.query(
            latest_chat_id.c.room_id.label("room_id"),
            latest_chat_id.c.latest_chat_id.label("latest_chat_id"),
            Chat.content.label("latest_chat_content"),
            User.nickname.label("latest_chat_user_name"),
            Chat.create_time.label("latest_chat_create_time"),
        ).outerjoin(Chat, (latest_chat_id.c.latest_chat_id == Chat.id))
        .outerjoin(User, (Chat.user_id == User.id))
    ).subquery()

    # Step 3: 最终查询 - 合并结果
    result = (
        db.session.query(
            room_list.c.room_id.label("room_id"),
            room_list.c.room_name.label("room_name"),
            new_msg_count.c.new_msg_count,
            latest_chat.c.latest_chat_id,
            latest_chat.c.latest_chat_content,
            latest_chat.c.latest_chat_user_name,
            latest_chat.c.latest_chat_create_time,
        )
        .outerjoin(
            new_msg_count,
            room_list.c.room_id == new_msg_count.c.room_id,
        )
        .outerjoin(
            latest_chat,
            room_list.c.room_id == latest_chat.c.room_id,
        )
    ).all()

    return result

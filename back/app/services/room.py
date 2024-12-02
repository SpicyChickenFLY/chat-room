from sqlalchemy.orm import aliased
from sqlalchemy.sql import func, case

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
    # Step 1: 子查询 - 获取每个房间的未读消息数量和最新消息ID
    new_msg_count_and_latest_chat_id = (
        db.session.query(
            UserRoomMap.room_id.label("room_id"),
            func.count(Chat.id).label("new_msg_count"),
            func.max(Chat.id).label("latest_chat_id"),
        )
        .outerjoin(
            Chat,
            (UserRoomMap.room_id == Chat.room_id)
            & (
                case(
                    (
                        UserRoomMap.last_confirm_chat_id.isnot(None),
                        UserRoomMap.last_confirm_chat_id,
                    ),
                    else_=0,
                )
                < Chat.id
            ),
        )
        .filter(UserRoomMap.user_id == user_id)
        .group_by(UserRoomMap.room_id)
    ).subquery()

    # Step 2: 子查询 - 获取每个房间的最新消息内容
    new_msg_count_and_latest_chat_content = (
        db.session.query(
            new_msg_count_and_latest_chat_id.c.room_id,
            new_msg_count_and_latest_chat_id.c.new_msg_count,
            Chat.content.label("latest_chat_content"),
            Chat.create_time.label("latest_chat_create_time")
        )
        .outerjoin(
            Chat,
            Chat.id == new_msg_count_and_latest_chat_id.c.latest_chat_id
        )
    ).subquery()

    # Step 3: 最终查询 - 合并结果
    result = (
        db.session.query(
            Room.id.label("room_id"),
            Room.name.label("room_name"),
            new_msg_count_and_latest_chat_content.c.new_msg_count,
            new_msg_count_and_latest_chat_content.c.latest_chat_content,
            new_msg_count_and_latest_chat_content.c.latest_chat_create_time
        ).outerjoin(
            new_msg_count_and_latest_chat_content,
            Room.id == new_msg_count_and_latest_chat_content.c.room_id,
        )
    ).all()

    return result

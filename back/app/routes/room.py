from flask import request
from flask_restful import Resource
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from app import services
from app import entities
from app.store import db

class RoomByUserApi(Resource):
    """房间成员列表"""

    def get(self, user_id):
        user = services.get_user(user_id)
        if user is None:
            return {"msg": "未查询到用户信息"}, 404

        # Subquery to find the latest chat for each room
        latest_chat_subquery = (
            db.session.query(
                entities.Chat.room_id,
                func.max(entities.Chat.id).label('max_id')
            )
            .group_by(entities.Chat.room_id)
            .subquery()
        )

        # Join the latest chat subquery with the chat table to get the latest chat content
        latest_chat_query = (
            db.session.query(
                entities.Chat.room_id,
                entities.Chat.id.label('latest_chat_id'),
                entities.Chat.content.label('latest_chat_content')
            )
            .join(latest_chat_subquery, (entities.Chat.room_id == latest_chat_subquery.c.room_id) & (entities.Chat.id == latest_chat_subquery.c.max_id))
            .subquery()
        )

        # Main query to get the user room info
        room_details = (
            db.session.query(
                entities.UserRoomMap.room_id,
                func.count(entities.Chat.id).label('unread_messages'),
                latest_chat_query.c.latest_chat_id,
                latest_chat_query.c.latest_chat_content
            )
            .outerjoin(entities.Chat, (entities.UserRoomMap.room_id == entities.Chat.room_id) & (entities.Chat.id > entities.UserRoomMap.last_confirm_chat_id))
            .outerjoin(latest_chat_query, entities.UserRoomMap.room_id == latest_chat_query.c.room_id)
            .filter(entities.UserRoomMap.user_id == user_id)
            .group_by(
                entities.UserRoomMap.room_id,
                latest_chat_query.c.latest_chat_id,
                latest_chat_query.c.latest_chat_content
            )
            .all()
        )

        return {
            "data": room_details
        }, 200

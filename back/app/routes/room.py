from flask import request
from flask_restful import Resource

from app import services


class RoomByUserApi(Resource):
    """房间成员列表"""

    def get(self, user_id):
        user = services.get_user(user_id)
        if user is None:
            return {"msg": "未查询到用户信息"}, 404

        room_details = services.get_room_details_for_user(user_id)

        return {
            "data": [
                {
                    "roomId": room_id,
                    "roomName": room_name,
                    "unreadMessages": unread_messages,
                    "latestChatContent": latest_chat_content,
                }
                for room_id, room_name, unread_messages, latest_chat_content in room_details
            ]
        }, 200

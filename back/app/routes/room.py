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
                    "latestChatId": latest_chat_id,
                    "latestChatContent": latest_chat_content,
                    "latestChatUserName": latest_chat_user_name,
                    "latestChatCreateTime": None if latest_chat_create_time is None else latest_chat_create_time.isoformat(),
                }
                for room_id, room_name, unread_messages, latest_chat_id, latest_chat_content, latest_chat_user_name, latest_chat_create_time in room_details
            ]
        }, 200

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful import request

from app import services


class ChatByRoomApi(Resource):
    """房间成员列表"""

    def get(self, room_id):
        # parser = RequestParser()
        # parser.add_argument("nextId", type="int")
        # parser.add_argument("limit")
        # args = parser.parse_args()
        args = request.args
        last_chat_id = args["nextId"]
        limit = args.get("limit", 50)
        chats = services.get_chat_for_room(room_id, last_chat_id, int(limit))

        data = [{"id": chat.id, "userId": chat.user_id, "content": chat.content, "createTime": None if chat.create_time is None else chat.create_time.isoformat()} for chat in chats]

        return {"data": data}, 200

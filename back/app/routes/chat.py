from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from flask_restful import request

from app import services


class ChatByRoomApi(Resource):
    """房间成员列表"""

    def get(self, room_id):
        parser = RequestParser()
        parser.add_argument("nextId", type="int")
        # parser.add_argument("limit")
        args = parser.parse_args()
        # args = request.args
        # last_chat_id = args["nextId"]
        # limit = args["limit"]
        # chats = services.get_chat_for_room(room_id, last_chat_id, limit)

        # return {"data": [{chat.id, chat.user_id, chat.content, chat.create_time} for chat in chats]}, 200
        return {"data": ""}, 200

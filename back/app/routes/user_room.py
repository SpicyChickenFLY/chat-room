from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug import security

from app import services
from app import entities
from app.entities.result import Result

class UserRoomApi(Resource):

    def post(self):
        """用户加入房间"""
        room_id=None
        user_id=None
        user_room = entities.UserRoom()(
            room_id=room_id,
            user_id=user_id
        )
        # services.create_user_room(user)
        return Result(msg="注册成功").to_dict(), 201



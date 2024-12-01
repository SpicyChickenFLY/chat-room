from flask import request
from flask_restful import Resource
from werkzeug import security

from app import services
from app import entities


class UsersApi(Resource):

    def post(self):
        """创建新用户"""
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if not username or not password:
            return {"msg": "用户名密码不能为空"}, 400
        user = services.find_user_by_nickname(username)
        if user is not None:
            return {"msg": "用户名已存在"}, 400

        user = entities.User()
        user.nickname = username
        user.token = security.generate_password_hash(password)
        services.create_user(user)

        user_room = entities.UserRoomMap()
        user_room.user_id = user.id
        user_room.room_id = 1
        user_room.authority = 1
        services.create_user_room(user_room)

        return {"msg": "登陆成功", "data": user.id}, 201


class UserApi(Resource):
    """注册"""

    def get(self, id):
        user = services.get_user(id)
        if user is None:
            return {"msg": "未查询到用户信息"}, 404
        return {
            "data": {
                "id": user.id,
                "nickname": user.nickname,
                "avatar": user.avatar,
                "status": user.status,
            }
        }, 200

class UserByRoomApi(Resource):
    """房间成员列表"""

    def get(self, room_id):
        pass

from flask import request
from flask_restful import Resource

from app import services
from app import entities


class UserRoomApi(Resource):
    def get(self, room_id: str, user_id: str):
        """获取用户房间映射关系"""
        user_room = services.get_user_room(user_id=user_id, room_id=room_id)
        if user_room is None:
            return {"msg": "用户不再该房间中"}, 404
        return {"msg": "获取成功", "data": user_room}, 200

    def post(self):
        """用户加入房间"""
        user_id = request.get_json()['userId']
        room_id = request.get_json()['roomId']
        user_room = entities.UserRoom()
        user_room.room_id=room_id
        user_room.user_id=user_id
        services.create_user_room(user_room)
        return {"msg": "注册成功"}, 201

    def put(self):
        """修改用户在房间中的设置信息"""

    def delete(self):
        """用户推出房间"""

class UserRoomsApi(Resource):
    def get(self):
        """获取用户房间映射关系列表"""
        user_id = request.get_json().get('userId')
        room_id = request.get_json().get('roomId')
        user_room = services.list_user_room(user_id=user_id, room_id=room_id)
        return { "data": user_room }, 200

    def delete(self):
        """解散房间或删除用户的连带映射处理"""


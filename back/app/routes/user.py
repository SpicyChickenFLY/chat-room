from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug import security

from app import services
from app import entities
from app.entities.result import Result

class UsersApi(Resource):

    def post(self):
        """创建新用户"""
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if not username or not password:
            return Result(msg="用户名密码不能为空").to_dict(), 400
        user = services.find_user_by_nickname(username)
        if user is not None:
            return Result(msg="用户名已存在").to_dict(), 400

        user = entities.User(
            nickname=username,
            token=security.generate_password_hash(password)
        )
        services.create_user(user)
        return Result(msg="注册成功").to_dict(), 201



class UserApi(Resource):
    """注册"""
    def get(self, id):
        user = services.get_user(id)
        if user is None:
            return Result(), 500
        return Result(msg="获取成功", data=user.id).to_dict(), 201




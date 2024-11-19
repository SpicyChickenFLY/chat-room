from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from sqlalchemy import Column
from werkzeug import security

from back.app import services
from back.app import entities
from back.app.entities.result import Result

users_db = {}


class RegisterApi(Resource):
    """注册"""

    def post(self):
        """获取管理器数据"""
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        if not username or not password:
            return Result(msg="用户名密码不能为空"), 400
        user = services.find_user()
        if user is not None:
            return Result(msg="用户名已存在"), 400

        user = entities.User(
            nickname=username, token=security.generate_password_hash(password)
        )
        services.create_user(user)
        return Result(msg="用户名已存在"), 201


class LoginApi(Resource):
    def post(self):
        """登陆"""
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"msg": "用户名和密码不能为空"}, 400
        user = services.find_user()
        if user is None:
            return {"msg": "用户名不存在"}, 401
        if not security.check_password_hash(user.user_token, password):
            return {"msg": "用户名或密码错误"}, 401

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 200

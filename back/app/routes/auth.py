from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug import security

from app import services
from app import entities

users_db = {}


class LoginApi(Resource):
    def post(self):
        """登陆"""
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        if not username or not password:
            return {"msg": "用户名密码不能为空"}, 400
        user = services.find_user_by_nickname(username)
        if user is None:
            return {"msg": "用户名不存在"}, 401
        if not security.check_password_hash(user.token, password):
            return {"msg": "用户名或密码错误"}, 401

        access_token = create_access_token(identity=user.id)
        return (
            {
                "msg": "登录成功",
                "data": {"accessToken": access_token},
            },
            200,
        )

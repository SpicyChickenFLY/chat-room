from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

users_db = {}

class RegisterApi(Resource):
    """注册"""
    def post(self):
        """获取管理器数据"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {"msg": "用户名和密码不能为空"}, 400
        if username in users_db:
            return {"msg": "用户已存在"}, 400
        users_db[username] = generate_password_hash(password)
        return {"msg": "注册成功"}, 201

class LoginApi(Resource):
    def post(self):
        """登陆"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {"msg": "用户名和密码不能为空"}, 400
        if username not in users_db:
            return {"msg": "用户名不存在"}, 401
        if not check_password_hash(users_db[username], password):
            return {"msg": "用户名或密码错误"}, 401
        access_token = create_access_token(identity=username)
        return { "access_token": access_token }, 200


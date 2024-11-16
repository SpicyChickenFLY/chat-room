"""页面的URL路由"""

from flask import session, redirect, url_for, render_template, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

from . import main

from flask_restful import Api, Resource


class Chat(Resource):
    @jwt_required()
    def post(self):
        """发送聊天"""



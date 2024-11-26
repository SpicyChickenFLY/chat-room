from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_restful import Api
from flask_cors import CORS

from .routes import api_add_resouces
from .store import init_db

app = Flask(__name__, static_folder="./static/assets/", template_folder="./static/")
CORS(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
api_add_resouces(Api(app))
init_db(app)


@app.route("/", methods=["GET"])
def index():
    """打开前端页面"""
    return render_template("index.html")


def run(debug=False):
    """Create an application."""
    app.debug = debug
    app.config["SECRET_KEY"] = "gjr39dkjn344_!67#"
    socketio.run(app, host="0.0.0.0", port=5000)

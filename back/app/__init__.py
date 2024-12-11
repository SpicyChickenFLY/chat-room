from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_cors import CORS

from .routes import init_api
from .store import init_db
from .events import init_socket, run_socket

app = Flask(__name__, static_folder="./static/assets/", template_folder="./static/")
app.config["SECRET_KEY"] = "gjr39dkjn344_!67#"
CORS(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
init_api(app)
init_db(app)
init_socket(app)


@app.route("/", methods=["GET"])
def index():
    """打开前端页面"""
    return render_template("index.html")


def run(debug=False):
    """Create an application."""
    app.debug = debug
    run_socket(app)

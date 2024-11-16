from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_restful import Api, Resource

from routes import auth

socketio = SocketIO()
app = Flask(__name__, static_folder="./static/assets/", template_folder="./static/")
app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

api = Api(app)
api.add_resource(auth.RegisterApi, 'auth/register')
api.add_resource(auth.LoginApi, 'auth/register')

@app.route("/", methods=["GET"])
def index():
    """打开前端页面"""
    return render_template("index.html")

def run(debug=False):
    """Create an application."""
    app.debug = debug
    socketio.init_app(app)
    return app


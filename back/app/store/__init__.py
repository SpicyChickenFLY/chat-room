from flask_sqlalchemy import SQLAlchemy

from .mysql import init_mysql_config

db = SQLAlchemy()
def init_db(app):
    init_mysql_config(app)
    db.init_app(app)


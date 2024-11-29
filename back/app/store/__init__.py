from flask_sqlalchemy import SQLAlchemy

from .mysql import get_mysql_uri

db = SQLAlchemy()
def init_db(app):
    conn_str = get_mysql_uri()
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()


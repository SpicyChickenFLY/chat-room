from app.store import db

class UserRoom(db.Model):
    __tablename__ = "user_room_map"

    user_id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, primary_key=True)
    authority = db.Column(db.Integer)
    mute = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

from app.store import db


class Room(db.Model):
    __tablename__ = "room_list"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    avatar = db.Column(db.String)
    single = db.Column(db.Boolean, default=False)
    create_time = db.Column(db.DateTime)

    user_room_maps = db.relationship('UserRoomMap',  back_populates="room")

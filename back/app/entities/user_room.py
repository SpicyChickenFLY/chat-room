from app.store import db

class UserRoomMap(db.Model):
    __tablename__ = "user_room_map"

    user_id = db.Column(db.Integer, db.ForeignKey('user_list.id'), primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room_list.id'), primary_key=True)
    authority = db.Column(db.Integer)
    mute = db.Column(db.Integer)
    last_confirm_chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    create_time = db.Column(db.DateTime)

    user = db.relationship('User', back_populates="user_room_maps")
    room = db.relationship('Room', back_populates="user_room_maps")

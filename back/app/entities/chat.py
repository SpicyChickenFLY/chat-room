from app.store import db

class Chat(db.Model):
    __tablename__ = 'chat_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_list.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('room_list.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

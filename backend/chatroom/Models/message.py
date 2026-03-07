from datetime import datetime
from backend.models.model_base.general_base import db



class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    status = db.Column(db.String(20), default="sent")  # sent / delivered

    user = db.relationship('User')
    room = db.relationship('Room')
from datetime import datetime
from backend.models.model_base.general_base import db
from .data import room_users

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship('User', secondary=room_users, backref='rooms')
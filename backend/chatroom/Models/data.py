from backend.models.model_base.general_base import db



room_users = db.Table(
    'room_users',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('room_id', db.Integer, db.ForeignKey('room.id'))
)
from datetime import datetime, timezone
from .general_base import db, RoleType, create_db
from ..security import generate_secret_key, generate_unique_key, reversible_hasher
from ...local_storage import localStorage as Storage

localStorage = Storage()
class User(db.Model):
    __tablename__ = "users" 
    
    id = db.Column(db.Integer, primary_key=True)

    # Identity
    name = db.Column(db.String(80), nullable=False, default="Anonymous")
    school_class = db.Column(db.String(50), nullable=False, default="Unassigned")

    # Roles
    role_type = db.Column(db.String(30), nullable=False, default=RoleType.GUEST)
    role_title = db.Column(db.String(80), nullable=True)

    # Session security
    session_key = db.Column(db.String(64), unique=True, index=True, nullable=False)
    key_updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Status
    is_active = db.Column(db.Boolean, default=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def rotate_key(self):
        self.session_key = generate_unique_key()
        self.secret_key = localStorage.getItem('ORC')
        self.key_updated_at = datetime.now(timezone.utc)
        db.session.commit()
        result_object = {'session_key': reversible_hasher(self.session_key, self.secret_key), 'secret_key': self.secret_key, 'updated_at': self.key_updated_at}
        return result_object
 

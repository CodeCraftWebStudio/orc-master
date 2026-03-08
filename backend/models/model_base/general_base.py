from ...Database import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {"check_same_thread": False}
}

db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)


class RoleType:
    GUEST = "guest"
    MEMBER = "member"
    NON_EDITOR_EXEC = "non_editor_exec"
    EDITING_EXEC = "editing_exec"
    ADMIN = "admin"


def create_db():
    with app.app_context():
        db.create_all()

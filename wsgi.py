from backend.Router import app, socketio
from backend.models.model_base.general_base import create_db

create_db()

if __name__ == "__main__":
    socketio.run(app)

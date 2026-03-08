import os
from backend.Router import app, socketio
from backend.models.model_base.general_base import create_db

if __name__ == "__main__":
    create_db()
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)

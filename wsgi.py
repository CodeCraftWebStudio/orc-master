from backend.Router import app
from backend.models.model_base.general_base import create_db

create_db()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

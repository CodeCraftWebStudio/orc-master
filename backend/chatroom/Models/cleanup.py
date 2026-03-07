import os
from datetime import datetime, timedelta
from .models import db, Message
DELETE_THRESHOLD = 0.05
SIZE_LIMIT = 1024 * 1024 * 1024
DATABASE_NAME = "chat.db"
def cleanup_if_needed():
    # Delete messages older than 24h
    cutoff = datetime.utcnow() - timedelta(hours=24)
    Message.query.filter(Message.timestamp < cutoff).delete()
    db.session.commit()

    # If DB > 1GB delete oldest 5%
    if os.path.exists(DATABASE_NAME):
        size = os.path.getsize(DATABASE_NAME)
        if size > 1 * SIZE_LIMIT:
            total = Message.query.count()
            to_delete = int(total * DELETE_THRESHOLD)

            oldest = Message.query.order_by(Message.timestamp).limit(to_delete).all()
            for msg in oldest:
                db.session.delete(msg)

            db.session.commit()
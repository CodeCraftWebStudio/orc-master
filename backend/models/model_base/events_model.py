from datetime import datetime, time
from .general_base import db

class CalendarEvent(db.Model):
    __tablename__ = "calendar_events"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, index=True)
    time = db.Column(db.Time, nullable=True)
    description = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        start = (
            f"{self.date}T{self.time.strftime('%H:%M')}"
            if self.time
            else str(self.date)
        )
        return {
            "id": self.id,
            "title": self.description,
            "date_obj": str(self.date),
            "time_obj": self.time.strftime("%H:%M") if self.time else None
        }

    @staticmethod
    def create(date_obj, time_obj, description_obj):
        event = CalendarEvent(
            date=date_obj,
            time=time.fromisoformat(time_obj) if time_obj else None,
            description=description_obj
        )
        db.session.add(event)
        db.session.commit()
        return event

    def update(self, new_time, new_description):
        self.time = time.fromisoformat(new_time) if new_time else self.time
        self.description = new_description or self.description
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    

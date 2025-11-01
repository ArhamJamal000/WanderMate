from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    travelers = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    mood = db.Column(db.String(50))
    preferences = db.Column(db.Text)
    itinerary = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'travelers': self.travelers,
            'budget': self.budget,
            'mood': self.mood,
            'preferences': self.preferences,
            'itinerary': self.itinerary,
            'created_at': self.created_at.isoformat()
        }

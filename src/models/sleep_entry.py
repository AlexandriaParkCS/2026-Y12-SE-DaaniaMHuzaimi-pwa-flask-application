from database import db
from datetime import datetime

class SleepEntry(db.Model):
    __tablename__ = 'sleep_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
    db. ForeignKey('users.id'), nullable=False)
    bedtime = db.Column(db.DateTime, nullable=False)
    wake_time = db.Column(db.DateTime, nullable=False)
    duration_hrs = db.Column(db.Float, nullable=False)
    quality = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def calculate_duration(bedtime, wake_time):
        delta = wake_time - bedtime
        return round(delta.total_seconds() / 3600, 2)

    @property
    def quality_label(self):
        labels = {1:'Very poor', 2:'Poor', 3:'Fair', 4:'Good', 5: 'Excellent'}
        return labels.get(self.quality, 'Unknown')

    @property
    def quality_colour(self):
        if self.quality >= 4:
            return 'success'
        elif self.quality == 3:
            return 'warning'
        return 'danger'

    def to_dict(self):
        return {
            'id': self.id,
            'duration_hrs': self.duration_hrs,
            'quality': self.quality,
            'date': self.bedtime.strftime('%d %b')
        }

class SleepGoal(db.Model):
    __tablename__ = 'sleep_goals'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    target_hours = db.Column(db.Float, default=8.0)
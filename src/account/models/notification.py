from datetime import datetime

from src.utils import db


class Notification(db.Model):
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: str = db.Column(db.String(255), nullable=False)
    message: str = db.Column(db.String(255), nullable=False)
    is_read: bool = db.Column(db.Boolean, nullable=False, default=False)
    available_at: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id: int = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

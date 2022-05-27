from dataclasses import dataclass
from datetime import datetime

from src.utils import db


@dataclass
class Account(db.Model):
    id: int = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name: str = db.Column(db.String(90), nullable=False)
    email: str = db.Column(db.String(18), nullable=False, unique=True)
    username: str = db.Column(db.String(14), nullable=False, unique=True)
    phone_number: str = db.Column(db.String(14), nullable=True)
    date_of_birth: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    date_join: datetime = db.Column(db.DateTime, nullable=False, default=datetime.now())
    last_signin: datetime = db.Column(db.DateTime, nullable=True)
    avatar: str = db.Column(db.String(90), nullable=True)
    password: str = db.Column(db.String(120), nullable=False)
    merchant: int = db.relationship('Merchant', backref='account', uselist=False)
    # notification = db.relationship('Notification', backref=db.backref('account', lazy='joined'), lazy='dynamic')

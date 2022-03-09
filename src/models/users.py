from dataclasses import dataclass
from datetime import datetime
import os

from src.utils import db


@dataclass
class Users(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email: str = db.Column(db.String(30), unique=True, nullable=False)
    username: str = db.Column(
        db.String(10), nullable=False, default=str(os.urandom(9)))
    date_join: db.DateTime = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    password: str = db.Column(db.String(130), nullable=False)
    address = db.relationship(
        'ShippingAddress', backref='users', lazy='dynamic')

    def __repr__(self) -> str:
        return "Username {}".format(self.username)


@dataclass
class ShippingAddress(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    address: str = db.Column(db.String(120), nullable=False)
    recipient_name: str = db.Column(db.String(15), nullable=False)
    active: bool = db.Column(db.Boolean, nullable=False, default=False)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self) -> str:
        return "address {}".format(self.address)

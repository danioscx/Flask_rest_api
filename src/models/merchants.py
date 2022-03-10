from dataclasses import dataclass
from datetime import datetime
import uuid
from src.utils import db


@dataclass
class Merchants(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(30), nullable=False)
    email: str = db.Column(db.String(30), nullable=False)
    username: str = db.Column(db.String(10), nullable=False, default=uuid.uuid4().hex[0:10])
    address: str = db.Column(db.String(120), nullable=False)
    phone_number: str = db.Column(db.String(15), nullable=False)
    # this is the token that the merchant will use to send push notifications to the app
    device_token: str = db.Column(db.String(130), nullable=True)
    is_verified: bool = db.Column(db.Boolean, nullable=False, default=False)
    passwrod: str = db.Column(db.String(130), nullable=False)
    products = db.relationship(
        'Products', backref='merchants', lazy='joined')
    open_time = db.relationship(
        'OpenTime', backref=db.backref('merchants', lazy='joined'), lazy=True)

    def __repr__(self) -> str:
        return "name {}".format(self.name)


@dataclass
class OpenTime(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant_id: int = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=False)
    day: str = db.Column(db.String(10), nullable=False)
    start_time: datetime = db.DateTime(db.DateTime, nullable=False)
    end_time: datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "day {}".format(self.day)
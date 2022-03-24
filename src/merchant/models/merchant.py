from dataclasses import dataclass
from datetime import datetime
import uuid
from src.utils import db


@dataclass
class Merchant(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant_name: str = db.Column(db.String(30), nullable=False)
    merchant_address: str = db.Column(db.String(120), nullable=False)
    is_verified: bool = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("account.id"))
    products = db.relationship(
        'Products', backref='merchant', lazy='joined')
    open_time = db.relationship(
        'OpenTime', backref=db.backref('merchant', lazy='joined'), lazy=True)

    def __repr__(self) -> str:
        return "name {}".format(self.name)


@dataclass
class OpenTime(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    merchant_id: int = db.Column(db.Integer, db.ForeignKey('merchants.id'), nullable=False)
    day: str = db.Column(db.String(10), nullable=False)
    is_open: bool = db.Column(db.Boolean, nullable=False, default=False)
    start_time: datetime = db.Column(db.DateTime, nullable=False)
    end_time: datetime = db.Column(db.DateTime, nullable=False)

    def __repr__(self) -> str:
        return "day {}".format(self.day)
from dataclasses import dataclass
from datetime import datetime
import uuid

from src.utils import db

relation_table = db.Table(
    'relation_table',
    db.Column('favorites_id', db.Integer, db.ForeignKey(
        'favorites.id'), primary_key=True),
    db.Column('products_id', db.Integer, db.ForeignKey(
        'products.id'), primary_key=True)
)


@dataclass
class Users(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email: str = db.Column(db.String(30), unique=True, nullable=False)
    username: str = db.Column(
        db.String(10), nullable=False, default=uuid.uuid4().hex[0:10])
    date_join: db.DateTime = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    password: str = db.Column(db.String(130), nullable=False)
    address = db.relationship(
        'ShippingAddress', backref='users', lazy='joined'
        )

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


@dataclass
class Favorites(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.relationship('Products', secondary=relation_table,
                              lazy='dynamic', backref=db.backref('favorite', lazy=True))
    times: db.DateTime = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    user_id: int = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False)

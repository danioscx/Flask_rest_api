from dataclasses import dataclass
from src.utils import db

@dataclass
class Merchant(db.Model):
    
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(30), nullable=False)
    email: str = db.Column(db.String(30), nullable=False)
    address: str = db.Column(db.String(120), nullable=False)
    phone_number: str = db.Column(db.String(15), nullable=False)
    device_token: str = db.Column(db.String(130), nullable=True) #this is the token that the merchant will use to send push notifications to the app
    is_verified: bool = db.Column(db.Boolean, nullable=False, default=False)
    passwrod: str = db.Column(db.String(130), nullable=False)
    products = db.relationship(
        'Products', backref='users', lazy='joined'
        )
    
    def __repr__(self) -> str:
        return "name {}".format(self.name)
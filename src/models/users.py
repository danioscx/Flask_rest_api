from dataclasses import dataclass
import os

from src.utils import db


@dataclass
class Users(db.Model):

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email: str = db.Column(db.String(30), unique=True, nullable=False)
    username: str = db.Column(db.String(10), nullable=False, default=os.urandom(9))
    password: str = db.Column(db.String(130), nullable=False)


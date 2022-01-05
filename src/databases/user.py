from dataclasses import dataclass

from src.databases import db


@dataclass
class User(db.Model):
    __tablename__ = "User"
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.String(20), nullable=False)
    email: str = db.Column(db.String(40), unique=True, nullable=False)
    password: str = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return "username {}".format(self.username)

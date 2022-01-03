from sqlalchemy.exc import SQLAlchemyError

from src import User, bcrypt
from src.databases import db


class UserModel(object):

    @staticmethod
    def create_user(username, email, password):
        try:
            db.session.add(
                User(username=username, email=email, password=bcrypt.generate_password_hash(password).decode('utf-8'))
            )
            db.session.commit()
            return True
        except SQLAlchemyError:
            return False

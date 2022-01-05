from sqlalchemy.exc import SQLAlchemyError

from src import User, bcrypt
from src.databases import db
from src.models import BaseModel


class UserModel(BaseModel):

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

    def get_users(self):
        response = User.query.with_entities(User.username).all()
        return self.object_to_list(response)

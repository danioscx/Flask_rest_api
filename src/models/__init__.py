from src import User, bcrypt
from src.databases import db


class UserModel(object):

    def __init__(self):
        self.user = User()
        self.db = db

    def sign_up(self, username: str, email: str, password: str) -> bool:
        create_user = self.db.session.add(User(username, email, bcrypt.generate_password_hash(password)))
        if create_user:
            self.db.session.commit()
            return True
        else:
            return False

    def get_user(self):
        return self.db.session.query(
            User.username,
            User.email
        ).all()

    def get_user_by_id(self):
        pass

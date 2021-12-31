import os

from flask import Flask

from src import jwt, bcrypt
from src.databases import db

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)
app.config["JWT_SECRET_KEY"] = os.urandom(20)
app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "/src/databases/default.sqlite"


def init_app():
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    return app


if __name__ == '__main__':
    app.run()

import os

from flask import Flask

from src import jwt, bcrypt
from src.databases.user import db
from src.routers import view


def app_main():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(10)
    app.config["JWT_SECRET_KEY"] = os.urandom(20)
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "/src/databases/default.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    app.register_blueprint(view)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    return app


def app_test():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.urandom(10)
    app.config["JWT_SECRET_KEY"] = os.urandom(20)
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.getcwd() + "/default.sqlite"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    app.register_blueprint(view)
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    return app

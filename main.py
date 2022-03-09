import os

from flask import Flask
from src.utils import db, bcrypt
from src.utils.jwt import jwt
from src.routers.users import users
from src.routers.address import address


def create_test_app():
    app = Flask(__name__)

    app.register_blueprint(users)
    app.register_blueprint(address)

    app.config['JWT_SECRET_KEY'] = 'supper-secret'
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/db.sqlite'.format(
        os.getcwd())
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    return app


def create_debug_app():
    app = Flask(__name__)

    app.register_blueprint(users)
    app.register_blueprint(address)

    app.config['JWT_SECRET_KEY'] = 'debug-secret'
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/db.sqlite'.format(
        os.getcwd())
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    return app


def create_release_app():
    app = Flask(__name__)

    app.register_blueprint(users)
    app.register_blueprint(address)

    app.config['JWT_SECRET_KEY'] = os.urandom(20)
    app.config["JWT_ERROR_MESSAGE_KEY"] = "message"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}/db.sqlite'.format(
        os.getcwd())
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    jwt.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    return app


if __name__ == "__main__":
    apps = create_test_app()
    apps.app_context().push()
    apps.run()

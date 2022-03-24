from dataclasses import asdict
import datetime
import decimal
import random

from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()
mail_app = Mail()


def default_encoder(obj):
    if isinstance(obj, decimal.Decimal):
        return str(obj)
    if isinstance(obj, bytes):
        return obj.decode('utf-8')
    if isinstance(obj, datetime.date):
        return obj.strftime('%Y-%m-%d')


def object_to_list(lists) -> list:
    result = []
    for value in lists:
        result.append(asdict(value))
    return result


class PasswordUtils(object):

    def __init__(self):
        self.password = None
        self.code_generator = None

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

    @staticmethod
    def __code_generator(length):
        return random.randint(10 ** (length - 1), (10 ** length) - 1)

    def get_code_generator(self):
        return self.code_generator

    def set_code_generator(self, length):
        self.code_generator = self.__code_generator(length)


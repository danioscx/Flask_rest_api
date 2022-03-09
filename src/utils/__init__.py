from dataclasses import asdict
import datetime
import decimal
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()


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

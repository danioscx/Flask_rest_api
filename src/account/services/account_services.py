from dataclasses import asdict
from datetime import datetime
from typing import Any

from src.account.models import Account
from src.utils import bcrypt, db, object_to_list


def get_user_by_id(account_id) -> Any:
    """
    :param account_id: ``user_id`` is must be ``int``
    :return: :class:~`src.account.models.Account` or None
    """
    return Account.query.filter_by(id=account_id).one_or_none()


def get_user_by_email(email) -> Any:
    """
    :param email: string
    :return: :class:~`src.account.models.Account` or None
    """
    return Account.query.filter_by(email=email).one_or_none()


def get_user_by_username(username) -> Any:
    """
    :param username: string
    :return: :class:~`src.account.models.Account` or None
    """
    return Account.query.filter_by(username=username).one_or_none()


def get_user_asdict(account_id) -> dict:
    """
    :param account_id: ``user_id`` is must be ``int``
    :return: `dict`
    """
    account = get_user_by_id(account_id)
    if account is not None:
        return asdict(account)
    else:
        return {}


def get_users_serialized() -> list:
    """
    :return: list of :class:~`src.account.models.Account`
    """
    return object_to_list(get_users())


def get_users() -> Any:
    """
    :return: empty list or list of :class:~`src.account.models.Account`
    """
    return Account.query.all()


def check_password(account, password) -> bool:
    """
    :param account: :class:~`src.account.model.Account`
    :param password: string
    :return: bool if password is correct, return ``True`` else ``False``
    """
    return bcrypt.check_password_hash(account.password, password)


def create_user(name, email, username, password, date_of_birth) -> bool:
    """
    :param name: string
    :param email: string
    :param username: string
    :param password: string
    :param date_of_birth: string
    :return: `bool`
    """
    try:
        account = Account(
            name=name,
            email=email,
            username=username,
            password=password,
            date_of_birth=datetime.strptime(date_of_birth, '%d/%m/%Y')
        )
        db.session.add(account)
        db.session.commit()
        return True
    except Exception as e:
        raise e


def delete_user(account_id) -> bool:
    """
    :param account_id: ``user_id`` is must be ``int``
    :return: `bool`
    """
    account = get_user_by_id(account_id)
    if account is not None:
        db.session.delete(account)
        db.session.commit()
        return True
    else:
        raise ValueError(f"Account with id {account_id} not found")

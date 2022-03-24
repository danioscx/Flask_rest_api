from src.account import Account
from src.utils import bcrypt


def get_user(account_id):
    """
    :param account_id: ``user_id`` is must be ``int``
    :return: :class:~`src.account.models.Account` or None
    """
    return Account.query.filter_by(id=account_id).one_or_none()


def get_users():
    """
    :return: empty list or list of :class:~`src.account.models.Account`
    """
    return Account.query.all()


def check_password(account, password) -> bool:
    """
    :param account: :class:~`src.account.model.Account`
    :param password: string
    :return: bool
    if password is correct, return ``True`` else ``False``
    """
    return bcrypt.check_password_hash(account.password, password)

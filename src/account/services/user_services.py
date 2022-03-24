from src.account import Account


class UserServices(object):

    def get_user(self, user_id):
        return Account.query.filter_by(id=user_id).one_or_none()

    def get_all_users(self):
        return Account.query.all()
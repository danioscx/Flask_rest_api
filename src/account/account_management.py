from flask import Flask


class AccountManagement(object):
    """
    This class is used to manage the account.
    """

    def __init__(self, app: Flask = None):
        """
        :param app: Flask app object
        """
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask):
        self._default_configuration(app)

    @staticmethod
    def _default_configuration(app: Flask):
        if 'SQLALCHEMY_DATABASE_URI' not in app.config:
            raise Exception('SQLALCHEMY_DATABASE_URI is not set')

    def register_model(self):
        pass


import unittest
import sys

sys.path.append("..")

from main import create_test_app
from src.utils import db


class BaseTest(unittest.TestCase):
    app = create_test_app()
    app.app_context().push()

    def setUp(self) -> None:
        db.create_all()

    def signup(self):
        return self.app.test_client().post('/api/v1/account/signup', json={
            'email': 'test@test.com',
            'username': "test",
            'password': "12345"
        })

    def signin(self):
        return self.app.test_client().post('/api/v1/account/signin', json={
            'email': 'test@test.com',
            'password': '12345'
        })

    def tearDown(self) -> None:
        db.drop_all()

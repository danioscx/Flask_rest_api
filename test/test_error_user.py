import unittest
import sys

sys.path.append("..")

from main import create_test_app
from src.utils import db



class TestErrorUser(unittest.TestCase):

    app = create_test_app()
    app.app_context().push()

    def setUp(self) -> None:
        db.create_all()

    def test_mal_signup(self):
        self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': "test",
            'password': "12345"
        })
        signup =  self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': "test",
            'password': "12345"
        })

        self.assertEqual(signup.status_code, 409)

    def test_mal_signin(self):
        self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': "test",
            'password': "12345"
        })
        #test with wrong email
        signin = self.app.test_client().post('/api/v1/user/signin', json={
            'email': 'test@test',
            'password': '12345'
        })

        self.assertEqual(signin.status_code, 409)

        #test with wrong password
        signin_password = self.app.test_client().post('/api/v1/user/signin', json={
            'email': 'test@test.com',
            'password': '1234'
        })

        self.assertEqual(signin_password.status_code, 409)


    def tearDown(self) -> None:
        db.drop_all()
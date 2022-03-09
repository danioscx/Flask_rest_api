
import unittest
import sys





sys.path.append("..")

from main import create_test_app
from src.utils import db



class UserTest(unittest.TestCase):

    apps = create_test_app()
    apps.app_context().push()

    def setUp(self) -> None:
        db.create_all()

    def test_sign_up(self):
        #test right success in
        signup_s = self.apps.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': 'tests',
            'password': '12345'
        })
        self.assertEqual(signup_s.status_code, 200)

    def test_user_sign_in(self):
        self.apps.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': 'tests',
            'password': '12345'
        })
        signin = self.apps.test_client().post('/api/v1/user/signin', json={
            'email':'test@test.com', 
            'password':'12345'
        })
        self.assertEqual(signin.status_code, 200)

    def test_signup_without_username(self):
        signup_s = self.apps.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'password': '12345'
        })
        self.assertEqual(signup_s.status_code, 200)


    def tearDown(self) -> None:
        db.drop_all()

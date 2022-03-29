from base_test import BaseTest


class AccountTest(BaseTest):

    def test_create_account(self):
        signup = self.app.test_client().post('/api/v1/accounts/signup', json={
            'name': 'test',
            'email': 'test@email.com',
            'username': 'test_user',
            'password': 'test_password',
            'date_of_birth': '01/01/2000',
        })
        print(signup.get_data(as_text=True))
        self.assertEqual(signup.status_code, 201)

import json
import unittest
from base_test import BaseTest


class UserTest(BaseTest):

    def test_sign_up(self):
        #test right success in
        signup_s = self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': 'tests',
            'password': '12345'
        })
        self.assertEqual(signup_s.status_code, 200)

    def test_user_sign_in(self):
        self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': 'tests',
            'password': '12345'
        })
        signin = self.app.test_client().post('/api/v1/user/signin', json={
            'email': 'test@test.com',
            'password': '12345'
        })
        self.assertEqual(signin.status_code, 200)

        #verify that we have access token when sign in is success
        json_data = json.loads(signin.get_data(as_text=True))
        self.assertTrue(json_data['token'] is not None)

    def test_signup_without_username(self):
        signup_s = self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'password': '12345'
        })
        self.assertEqual(signup_s.status_code, 200)

    def test_get_user(self):
        #create account first
        signup_s = self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': 'tests',
            'password': '12345'
        })
        #make sure we success signup
        self.assertEqual(signup_s.status_code, 200)

        signin = self.app.test_client().post('/api/v1/user/signin', json={
            'email': 'test@test.com',
            'password': '12345'
        })
        #make sure we success signin
        self.assertEqual(signin.status_code, 200)

        access_token = json.loads(signin.get_data(as_text=True))
        if access_token is not None:
            user = self.app.test_client().get('/api/v1/user/me', headers={
                "Authorization": "Bearer {}".format(access_token['token'])
            })
            self.assertEqual(user.status_code, 200)

    def test_mal_signup(self):
        self.app.test_client().post('/api/v1/user/signup', json={
            'email': 'test@test.com',
            'username': "test",
            'password': "12345"
        })
        signup = self.app.test_client().post('/api/v1/user/signup', json={
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

        #verify that we dont have token when email is wrong
        responses = signin.get_data(as_text=True)
        self.assertFalse("token" in responses)

        #test with wrong password
        signin_password = self.app.test_client().post('/api/v1/user/signin', json={
            'email': 'test@test.com',
            'password': '1234'
        })

        self.assertEqual(signin_password.status_code, 409)

        #verify that we dont have access token when password is wrong
        response_password = signin_password.get_data(as_text=True)
        self.assertFalse("token" in response_password)


class UserTestUpdateInsert(BaseTest):

    def test_add_address(self):
        sign_up = self.signup()
        self.assertEqual(sign_up.status_code, 200)
        sign_in = self.signin()
        self.assertEqual(sign_in.status_code, 200)

        access_token = json.loads(sign_in.get_data(as_text=True))
        if access_token is not None:
            add = self.app.test_client().put(
                '/api/v1/address/add',
                headers={
                    "Authorization": "Bearer {}".format(access_token['token'])
                },
                json={
                    'recipient_name': 'Ramdhany',
                    'address': 'test address'
                }
            )
            #check if status code is 200
            self.assertEqual(add.status_code, 200)

            response = add.get_data(as_text=True)
            #make sure that response contains success string
            self.assertTrue("success" in response)

            #test success update address
            update_address = self.app.test_client().patch("/api/v1/address/update/1", 
                headers={
                    "Authorization": "Bearer {}".format(access_token['token'])
                },
                json={
                    "address": "address test 2",
                    "recipient_name": "oscop",
                    "active": True
                }
            )
            response_update = update_address.get_data(as_text=True) 
            self.assertEqual(update_address.status_code, 200)
            self.assertTrue("success update" in response_update)
            
            #add new address
            second = self.app.test_client().put(
                '/api/v1/address/add',
                headers={
                    "Authorization": "Bearer {}".format(access_token['token'])
                },
                json={
                    'recipient_name': 'Budi',
                    'address': 'test address 2'
                }
            )
            #check if status code is 200
            self.assertEqual(second.status_code, 200)

            response_second = second.get_data(as_text=True)
            #make sure that response contains success string
            self.assertTrue("success" in response_second)
            
            #get address 
            get_address = self.app.test_client().get(
                "/api/v1/address/get",
                 headers={
                    "Authorization": "Bearer {}".format(access_token['token'])
                }
            )
            self.assertEqual(get_address.status_code, 200)
            response_address = get_address.get_data(as_text=True)
            self.assertTrue("Budi" in response_address)
            self.assertTrue("oscop" in response_address)
            #test delete address
            del_address = self.app.test_client().delete(
                "/api/v1/address/delete/2",
                 headers={
                    "Authorization": "Bearer {}".format(access_token['token'])
                }
            )
            self.assertEqual(del_address.status_code, 200)


if __name__ == "__main__":
    unittest.main()

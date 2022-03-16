from base_test import BaseTest


class MerchantTests(BaseTest):
    
    def test_signup(self):
        response = self.app.test_client().post(
            "/api/v1/merchants/signup",
            json={
                "name": "test",
                "email": "email@email",
                "username": "username",
                "address": "address",
                "phone_number": "123456789",
                "password": "12345"
            }
        )
        
        self.assertEqual(response.status_code, 201)
        pass
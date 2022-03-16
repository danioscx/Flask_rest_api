
from base_test import BaseTest


class TestProducts(BaseTest):
    
    def test_get_products(self):
        """
        Test get products
        """
        
        """
        User signin and signup
        """
        sign_up = self.signup()
        self.assertEqual(sign_up.status_code, 200)
        sign_in = self.signin()
        self.assertEqual(sign_in.status_code, 200)
        
    pass

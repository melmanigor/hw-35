import unittest
from app import app
import json
from cart.cart_routes import cart
from flask import session

class TestCart(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        cart.clear()

    def test_cart_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_item(self):
        response = self.client.post('/api/items', json={'item': 'banana'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('banana',cart)
    
    def tes_add_item_session(self):



if __name__ == '__main__':
    unittest.main()

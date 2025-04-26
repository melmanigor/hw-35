import unittest
from app import app
import json
from flask import session


class TestCart(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_cart_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_add_item(self):
    #     response = self.client.post('/api/items', json={'item': 'banana'})
    #     self.assertEqual(response.status_code, 201)
    #     self.assertIn('banana', cart)

    def test_add_item_session(self):
        
        with self.client as client:
            client.post('/cart/',data={'item':'banana','quantity':1})
            client.post('/cart/update_quantity', data={'item':'banana','delta':1})
        
        with client.session_transaction() as sess:
            cart=sess.get('cart',[])
          
            banana = next(
                    (
                        item
                        for item in cart
                        if item['name'].lower() == 'banana'
                    ),
                    None
                )
            self.assertIsNotNone(banana)
            self.assertEqual(banana['quantity'], 2)
    
    def test_log_out(self):
        with self.client as client:
            response=client.get('/logout',follow_redirects=True)
            self.assertGreater(len(response.history),0)
            self.assertEqual(response.request.path,'/')


          


if __name__ == '__main__':
    unittest.main()

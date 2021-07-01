import unittest

from app.main import db
from app.main.model.product import Product
from app.main.model.blacklist import BlacklistToken
import json
from app.test.base import BaseTestCase

def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            username='usernamec',
            password='123456',
            role='buyer'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            username='usernamec',
            password='123456'
        )),
        content_type='application/json'
    )

def register_user_seller(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            username='usernamed',
            password='123456',
            role='seller'
        )),
        content_type='application/json'
    )


def login_user_seller(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            username='usernamed',
            password='123456'
        )),
        content_type='application/json'
    )

class TestUserEndpoints(BaseTestCase):
    def test_create_user(self):
        response = self.client.post(
            '/user/',
            data=json.dumps(dict(
                username='usernameb',
                password='123456',
                role='buyer'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_users_no_login(self):
        # get users
        response = self.client.get('/user/')
        
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Provide a valid auth token.')
        self.assertEqual(response.status_code, 401)

    def test_get_users(self):
        # user registration
        resp_register = register_user(self)
        # registered user login
        resp_login = login_user(self)
        data = json.loads(resp_login.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        # get users
        response = self.client.get(
            '/user/',
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['data'])
        self.assertEqual(response.status_code, 200)

    def test_deposit(self):
        # user registration
        resp_register = register_user(self)
        # registered user login
        resp_login = login_user(self)
        data = json.loads(resp_login.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        response = self.client.post(
            '/user/deposit',
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            ),
            data=json.dumps(dict(
                amount=1
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Deposit successful.')
        self.assertEqual(response.status_code, 200)

    def test_reset(self):
        # user registration
        resp_register = register_user(self)
        # registered user login
        resp_login = login_user(self)
        data = json.loads(resp_login.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        response = self.client.post(
            '/user/reset',
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Deposit reset successful.')
        self.assertEqual(response.status_code, 200)

    def test_buy(self):
        # user registration
        resp_register = register_user_seller(self)
        # registered user login
        resp_login = login_user_seller(self)
        data = json.loads(resp_login.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        # Create product
        response = self.client.post(
            '/product/',
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            ),
            data=json.dumps(dict(
                amount_available=10,
                cost=1,
                product_name='test_product'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['amount_available'] == 10)
        self.assertTrue(data['cost'] == 1)
        self.assertTrue(data['product_name'] == 'test_product')
        self.assertEqual(response.status_code, 201)
        
        product_id = data['id']

        # Login as buyer
        # user registration
        resp_register = register_user(self)
        # registered user login
        resp_login = login_user(self)
        data = json.loads(resp_login.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        # deposit
        response = self.client.post(
            '/user/deposit',
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            ),
            data=json.dumps(dict(
                amount=1
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Deposit successful.')
        self.assertEqual(response.status_code, 200)

        # buy
        response = self.client.post(
            '/user/buy',
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            ),
            data=json.dumps(dict(
                product_id=product_id,
                amount=1,
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['spent'] == 1)
        self.assertTrue(data['change'] == 0)
        self.assertTrue(data['products_bought'] == 1)
        self.assertEqual(response.status_code, 200)
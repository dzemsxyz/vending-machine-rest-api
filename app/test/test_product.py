import unittest

from app.main import db
import json
from app.test.base import BaseTestCase

def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            username='usernameb',
            password='123456',
            role='buyer'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            username='usernameb',
            password='123456'
        )),
        content_type='application/json'
    )

def register_user_seller(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            username='usernames',
            password='123456',
            role='seller'
        )),
        content_type='application/json'
    )


def login_user_seller(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            username='usernames',
            password='123456'
        )),
        content_type='application/json'
    )


class TestProductEndpoints(BaseTestCase):

    def test_create_product_non_seller(self):
        # user registration
        resp_register = register_user(self)
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(
            data_register['message'] == 'Successfully registered.'
        )
        self.assertTrue(data_register['Authorization'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)
        # registered user login
        resp_login = login_user(self)
        data = json.loads(resp_login.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged in.')
        self.assertTrue(data['Authorization'])
        self.assertTrue(resp_login.content_type == 'application/json')
        self.assertEqual(resp_login.status_code, 200)

        # Try to create product with buyer role
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
        self.assertTrue(data['status'] == 'fail')
        self.assertTrue(data['message'] == 'Only seller users can access this endpoint')
        self.assertEqual(response.status_code, 401)
        
    def test_create_product_seller_and_update(self):
        # user registration
        resp_register = register_user_seller(self)
        data_register = json.loads(resp_register.data.decode())
        self.assertTrue(data_register['status'] == 'success')
        self.assertTrue(
            data_register['message'] == 'Successfully registered.'
        )
        self.assertTrue(data_register['Authorization'])
        self.assertTrue(resp_register.content_type == 'application/json')
        self.assertEqual(resp_register.status_code, 201)
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

        
    def test_list_products(self):
        response = self.client.get(
            '/product/'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['data'] is not None)
        self.assertEqual(response.status_code, 200)

    def test_create_product_seller_and_update(self):
        # user registration
        register_user_seller(self)
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
                product_name='test_product_update'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['amount_available'] == 10)
        self.assertTrue(data['cost'] == 1)
        self.assertTrue(data['product_name'] == 'test_product_update')
        self.assertEqual(response.status_code, 201)

        product_id = data['id']

        # update product
        response = self.client.put(
            '/product/'+str(product_id),
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            ),
            data=json.dumps(dict(
                id=product_id,
                amount_available=9,
                cost=0.5,
                product_name='test_product_update_2'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['id'] == product_id)
        self.assertTrue(data['amount_available'] == 9)
        self.assertTrue(data['cost'] == 0.5)
        self.assertTrue(data['product_name'] == 'test_product_update_2')
        self.assertEqual(response.status_code, 200)

    def test_get_product_by_id(self):
        # user registration
        register_user_seller(self)
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
                product_name='test_product_get'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['amount_available'] == 10)
        self.assertTrue(data['cost'] == 1)
        self.assertTrue(data['product_name'] == 'test_product_get')
        self.assertEqual(response.status_code, 201)

        product_id = data['id']

        # get product
        response = self.client.get(
            '/product/'+str(product_id),
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['id'] == product_id)
        self.assertTrue(data['amount_available'] == 10)
        self.assertTrue(data['cost'] == 1)
        self.assertTrue(data['product_name'] == 'test_product_get')
        self.assertEqual(response.status_code, 200)

    def test_delete_product(self):
        # user registration
        register_user_seller(self)
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
                product_name='test_product_delete'
            )),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['amount_available'] == 10)
        self.assertTrue(data['cost'] == 1)
        self.assertTrue(data['product_name'] == 'test_product_delete')
        self.assertEqual(response.status_code, 201)

        product_id = data['id']

        # delete product
        response = self.client.delete(
            '/product/'+str(product_id),
            headers=dict(
                Authorization=json.loads(
                    resp_login.data.decode()
                )['Authorization']
            )
        )
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Product deleted.')
        self.assertEqual(response.status_code, 200)
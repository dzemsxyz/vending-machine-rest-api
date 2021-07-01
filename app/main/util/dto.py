from flask.globals import request
from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'id': fields.Integer(readonly=True, description='user identifier'),
        'username': fields.String(required=True, description='user username'),
        'deposit': fields.Float(required=False, description='the deposit'),
        'password': fields.String(required=True, description='user password'),
        'role': fields.String(required=True, description='user role')
    })
    register = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password')
    })
    deposit = api.model('deposit', {
        'amount': fields.Float(required=True, description='amount to deposit')
    })
    buy = api.model('buy', {
        'product_id': fields.Integer(required=True, description='product identifier'),
        'amount': fields.Integer(required=True, description='amount of products')
    })

class ProductDto:
    api = Namespace('product', description='product related operations')
    product = api.model('product', {
        'id': fields.Integer(readonly=True, description='product identifier'),
        'amount_available': fields.Integer(required=True, description='amount available'),
        'cost': fields.Float(required=True, description='cost of product'),
        'product_name': fields.String(required=True, description='product name')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'username': fields.String(required=True, description='The username'),
        'password': fields.String(required=True, description='The user password '),
    })

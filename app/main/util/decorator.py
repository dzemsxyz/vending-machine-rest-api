from app.main.model.product import Product
from app.main.model import user
from functools import wraps

from flask import request

from app.main.service.auth_helper import Auth
from typing import Callable
    

def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated

def seller_role_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, _ = Auth.get_logged_in_user(request)
        role = data.get('data').get('role')

        if role != 'seller':
            response_object = {
                'status': 'fail',
                'message': 'Only seller users can access this endpoint'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

def buyer_role_required(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, _ = Auth.get_logged_in_user(request)
        role = data.get('data').get('role')

        if role != 'buyer':
            response_object = {
                'status': 'fail',
                'message': 'Only buyer users can access this endpoint'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

def seller_token_required_for_product(f: Callable) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_user(request)
        user_id = data.get('data').get('user_id')
        product_id = request.view_args.get('id')
        product = Product.query.filter_by(id=product_id).one_or_none()

        if not product:
            return data, status

        if product.seller_id != user_id:
            response_object = {
                'status': 'fail',
                'message': 'Only seller of the product can access this endpoint'
            }
            return response_object, 401

        return f(*args, **kwargs)

    return decorated

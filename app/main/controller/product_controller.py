from app.main.controller.user_controller import User
from flask import request
from flask_restx import Resource
from app.main.util.decorator import seller_token_required_for_product, seller_role_required, token_required

from app.main.service.auth_helper import Auth
from ..util.dto import ProductDto
from ..service.product_service import save_product, get_all_products, get_product, delete_product, update_product
from typing import Dict, Tuple

api = ProductDto.api
_product = ProductDto.product


@api.route('/')
class ProductList(Resource):
    @api.doc('list_of_products')
    @api.marshal_list_with(_product, envelope='data')
    def get(self):
        """List all products"""
        return get_all_products()

    @api.expect(_product, validate=True)
    @api.response(201, 'Product successfully created.')
    @api.doc('create a new product')
    @token_required
    @seller_role_required
    @api.marshal_with(_product) 
    def post(self):
        """Creates a new Product """
        user, _ = Auth.get_logged_in_user(request)
        data = request.json
        data['seller_id'] = user['data']['user_id']
        return save_product(data=data)

@api.route('/<id>')
@api.param('id', 'The Product identifier')
@api.response(404, 'Product not found.')
class Product(Resource):
    @api.doc('get a product')
    @api.marshal_with(_product)
    def get(self, id):
        """get a product given its identifier"""
        product = get_product(id)
        if not product:
            api.abort(404)
        else:
            return product
    
    @api.expect(_product, validate=True)
    @api.response(200, 'Product successfully updated.')
    @api.doc('update product')
    @api.marshal_with(_product)
    @token_required
    @seller_token_required_for_product
    def put(self, id):
        """Update Product """
        data = request.json
        return update_product(data, id)

    @api.doc('delete a product')
    @api.response(200, 'Product successfully deleted.')
    @token_required
    @seller_token_required_for_product
    def delete(self, id):
        """delete a product given its identifier"""
        return delete_product(id)

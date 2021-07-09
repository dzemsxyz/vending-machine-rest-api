from flask import request
from flask_restx import Resource

from app.main.util.decorator import token_required, buyer_role_required
from app.main.service.auth_helper import Auth
from ..util.dto import UserDto
from ..service.user_service import (
    save_user,
    get_all_users,
    get_user,
    delete_user,
    update_user,
    deposit,
    buy,
    reset_deposit
)
from typing import Dict, Tuple

api = UserDto.api
_user = UserDto.user
_user_update = UserDto.user_update
_deposit = UserDto.deposit
_buy = UserDto.buy

@api.route('/')
class UserList(Resource):
    @api.doc('list_of_registered_users')
    @token_required
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.expect(_user, validate=True)
    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    def post(self) -> Tuple[Dict[str, str], int]:
        """Creates a new User """
        data = request.json
        return save_user(data=data)

@api.route('/<id>')
@api.param('id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    @token_required
    def get(self, id):
        """get a user given its identifier"""
        user = get_user(id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.expect(_user_update, validate=True)
    @api.response(200, 'User successfully updated.')
    @api.doc('update user')
    @api.marshal_with(_user)
    @token_required
    def put(self, id) -> Tuple[Dict[str, str], int]:
        """Updates User """
        data = request.json
        return update_user(data, id)
    
    @api.doc('delete user')
    @token_required 
    @api.response(204, 'User successfully deleted.')
    def delete(self, id):
        """delete an user given its identifier"""
        success = delete_user(id)
        if not success:
            api.abort(404)
        else:
            return 204

@api.route('/deposit')
class UserDeposit(Resource):
    @api.expect(_deposit, validate=True)
    @api.response(200, 'Deposit successfully updated.')
    @api.doc('updated deposit')
    @token_required
    @buyer_role_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """Updates deposit of user """
        data = request.json
        user = Auth.get_logged_in_user_object(request)
        return deposit(data, user)

@api.route('/buy')
class UserBuy(Resource):
    @api.expect(_buy, validate=True)
    @api.response(200, 'Products successfully bought.')
    @api.doc('products bought')
    @token_required
    @buyer_role_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """Endpoint to buy products """
        data = request.json
        user = Auth.get_logged_in_user_object(request)
        return buy(data, user)

@api.route('/reset')
class UserResetDeposit(Resource):
    @api.response(200, 'Deposit successfully reset.')
    @api.doc('reset deposit')
    @token_required
    @buyer_role_required
    def post(self) -> Tuple[Dict[str, str], int]:
        """Endpoint to reset deposit """
        user = Auth.get_logged_in_user_object(request)
        return reset_deposit(user)
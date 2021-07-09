import uuid
import datetime

from app.main import db
from app.main.model.user import User, UserRoleEnum
from app.main.model.product import Product
from app.main.service.product_service import save_changes as save_product
from typing import Dict, Tuple

allowed_coins = [1, 0.5, 0.2, 0.1, 0.05]

def amount_to_coins(amount):
    coins = []
    while amount >= 0.05:
        for coin in allowed_coins:
            if coin <= amount:
                coins.append(coin)
                amount=round(amount-coin, 2)
                break
    return coins

def save_user(data: Dict[str, str]) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            username=data['username'],
            deposit=0,
            password=data['password'],
            role=UserRoleEnum[data['role']].value
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409

def update_user(data: Dict[str, str], id) -> Tuple[Dict[str, str], int]:
    user = User.query.filter_by(id=id).first()
    if user:
        if 'username' in data:
            user.username=data['username']
        save_changes(user)
        return user, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 404

def deposit(data: Dict[str, str], user) -> Tuple[Dict[str, str], User]:
    amount = data['amount']
    if user and amount in allowed_coins:
        user.deposit=user.deposit+amount
        save_changes(user)
        
        response_object = {
            'status': 'success',
            'message': 'Deposit successful.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'Deposit failed.',
        }
        return response_object, 400

def buy(data: Dict[str, str], user) -> Tuple[Dict[str, str], int]:
    product = Product.query.filter_by(id=data['product_id']).first()
    if user and product:
        final_cost = product.cost * data['amount']

        if product.amount_available < data['amount']:
            response_object = {
                'status': 'fail',
                'message': 'Not enough products in storage.',
            }
            return response_object, 400
        if user.deposit < final_cost:
            response_object = {
                'status': 'fail',
                'message': 'You have insufficient funds for this purchase.',
            }
            return response_object, 400

        user.deposit=user.deposit-final_cost
        product.amount_available = product.amount_available - data['amount']
        save_changes(user)
        save_product(product)
        response_object = {
            'spent': final_cost,
            'change': amount_to_coins(user.deposit),
            'products_bought': data['amount'],
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User or product not found.',
        }
        return response_object, 404

def reset_deposit(user):
    if user:
        user.deposit = 0
        save_changes(user)
        response_object = {
            'status': 'success',
            'message': 'Deposit reset successful.',
        }
        return response_object, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 404


def get_all_users():
    return User.query.all()


def get_user(id):
    return User.query.filter_by(id=id).first()


def delete_user(id):
    try:
        User.query.filter_by(id=id).delete()
        db.session.commit()
        return True
    except:
        return False

def generate_token(user: User) -> Tuple[Dict[str, str], int]:
    try:
        # generate the auth token
        auth_token = User.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401


def save_changes(data: User) -> None:
    db.session.add(data)
    db.session.commit()


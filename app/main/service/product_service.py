import uuid
import datetime

from app.main import db
from app.main.model.product import Product
from typing import Dict, Tuple

def save_product(data) -> Tuple[Dict, int]:
    new_product = Product(
        amount_available=data['amount_available'],
        product_name=data['product_name'],
        cost=data['cost'],
        seller_id=data['seller_id']
    )
    save_changes(new_product)
    return new_product, 201

def update_product(data, id) -> Tuple[Dict, int]:
    product = Product.query.filter_by(id=id).one_or_none()
    if product:
        if 'amount_available' in data:
            product.amount_available=data['amount_available']
        if 'product_name' in data:
            product.product_name=data['product_name']
        if 'cost' in data:
            product.cost=data['cost']
        save_changes(product)
        return product, 200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User does not exist.',
        }
        return response_object, 404


def get_all_products():
    return Product.query.all()

def get_product(id):
    return Product.query.filter_by(id=id).first()

def delete_product(id):
    try:
        product = Product.query.filter_by(id=id)
        if product:
            product.delete()
        else: 
            raise Exception
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Product deleted.',
        }
        return response_object, 200
    except:
        response_object = {
            'status': 'fail',
            'message': 'Product does not exist.',
        }
        return response_object, 404
    

def save_changes(data: Product) -> None:
    db.session.add(data)
    db.session.commit()
from sqlalchemy.orm import composite
from .. import db
import datetime


class Product(db.Model):
    """
    Product model
    """
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    amount_available = db.Column(db.Integer)
    cost = db.Column(db.Float)
    product_name = db.Column(db.String(50))
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))

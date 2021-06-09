from datetime import datetime

from sqlalchemy.orm import backref
from api.db.database import db


cart_product = db.Table('cart_product',
  db.Column('cart_id', db.Integer, db.ForeignKey('cart.id'), primary_key=True),
  db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True),
  db.Column('quantity', db.Integer, nullable=False),
  db.Column('price', db.Float, nullable=False),
  db.Column('total_discount', db.Float, nullable=False)
)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float, nullable=False, default=0.0)
    finished = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    products = db.relationship(
      'Product',
      secondary=cart_product,
      lazy='subquery',
      backref=db.backref('carts', lazy=True))

    def __iter__(self):
        data = {
            "id": self.id,
            "total": self.total,
            "finished": self.finished,
            "date": datetime.strftime(self.available_date, '%Y-%m-%d')
        }
        for key, value in data.items():
            yield key, value

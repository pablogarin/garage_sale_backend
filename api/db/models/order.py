from datetime import datetime
import uuid

from sqlalchemy.orm import relationship
from api.db.database import db


class OrderProduct(db.Model):
  order_id = db.Column(db.Integer, db.ForeignKey('order.id'), primary_key=True)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
  quantity = db.Column(db.Integer, nullable=False)
  price = db.Column(db.Float, nullable=False)
  total_discount = db.Column(db.Float, nullable=False)
  product = relationship("Product")


class Order(db.Model):
    id = db.Column(db.String(32), primary_key=True, default=lambda: f"{uuid.uuid4()}")
    total = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String, nullable=False, default='created')
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship("OrderProduct", lazy="subquery")

    def __iter__(self):
        data = {
            "id": self.id,
            "total": self.total,
            "status": self.status,
            "date": datetime.strftime(self.date, '%Y-%m-%d'),
            "products": [{
              **dict(prd.product),
              "quantity": prd.quantity,
              "totalDiscount": prd.total_discount,
              "unit_price": prd.price,
              "total_price": prd.price*prd.quantity,
            } for prd in self.products]
        }
        for key, value in data.items():
            yield key, value

from datetime import datetime
from api.db.database import db


class ProductStock(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    available = db.Column(db.Integer, nullable=False, default=0)
    reserved = db.Column(db.Integer, nullable=False, default=0)


class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    url = db.Column(db.String(120), nullable=False)
    order = db.Column(db.Float, default=0.0)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    available_date = db.Column(db.DateTime, nullable=False)
    category = db.relationship("CategoryProduct", lazy="subquery")
    images = db.relationship("ProductImage", lazy="subquery")
    stock = db.relationship("ProductStock", uselist=False, lazy="subquery")

    def __iter__(self):
        data = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "images": [img.url for img in self.images],
            "description": self.description,
            "availableDate": datetime.strftime(self.available_date, '%Y-%m-%d'),
            "stock": self.stock.available - self.stock.reserved
        }
        for key, value in data.items():
            yield key, value

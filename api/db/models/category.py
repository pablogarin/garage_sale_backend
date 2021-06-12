from sqlalchemy.orm import relationship
from api.db.database import db


class CategoryProduct(db.Model):
  category_id = db.Column(db.Integer, db.ForeignKey("category.id"), primary_key=True)
  product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)
  product = relationship("Product")


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    products = relationship("CategoryProduct", lazy="subquery")

    def __iter__(self):
        data = {
            "id": self.id,
            "name": self.name
        }
        for key, value in data.items():
            yield key, value

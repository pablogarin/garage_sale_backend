from datetime import datetime
from flask import Response
import json
from api.db.database import db
from api.db.models.category import Category
from api.db.models.category import CategoryProduct
from api.db.models.product import Product
from api.db.models.product import ProductStock
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError


class ProductResource(Resource):
    _id_key = "product_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, product_id=None):
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            raise ResourceNotFoundError()
        response = dict(product)
        if self._request.args.get("category") == "1":
          response["category"] = dict(product.category[0].category)
        self._response.set_data(json.dumps(response))

    def get_all(self):
        categories = Product.query.all()
        self._response.set_data(json.dumps([dict(c) for c in categories]))

    def create(
            self,
            name=None,
            price=None,
            image=None,
            description=None,
            available_date=None,
            category_id=None,
            stock=None):
        date_object = datetime.strptime(available_date, '%Y-%m-%d')
        product = Product(
            name=name,
            price=price,
            image=image,
            description=description,
            available_date=date_object)
        product_stock = ProductStock(available=(stock if stock else 1))
        product.stock = product_stock
        if category_id:
          category = Category.query.filter_by(id=category_id).first()
          if category:
            product.category = [CategoryProduct(category=category, product=product)]
        self._database.session.add(product)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(product)))

    def update(
            self,
            product_id=None,
            name=None,
            price=None,
            image=None,
            description=None,
            available_date=None,
            category_id=None,
            stock=None):
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            raise ResourceNotFoundError()
        if product:
            product.name = name if name else product.name
            product.price = price if price else product.price
            product.image = image if image else product.image
            product.description = \
              description if description else product.description
            product.available_date = \
              datetime.strptime(available_date, '%Y-%m-%d')\
              if available_date\
              else product.available_date
            product_stock = ProductStock.query.filter_by(product_id=product_id).first()
            product_stock.available = stock if stock else product_stock.available
            product.stock = product_stock
            if category_id:
              product_category = CategoryProduct.query.filter_by(product_id=product_id).first()
              if product_category:
                product_category.category_id = category_id
              else:
                category = Category.query.filter_by(id=category_id).first()
                if category:
                  product_category = CategoryProduct(category=category, product=product)
              if product_category:
                product.category = [product_category]
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(product)))
        

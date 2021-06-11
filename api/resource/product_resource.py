from datetime import datetime
from flask import Response
import json
from api.db.database import db
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
    
    def get(self, id):
        product = Product.query.filter_by(id=id).first()
        if not product:
            raise ResourceNotFoundError()
        self._response.set_data(json.dumps(dict(product)))

    def get_all(self):
        categories = Product.query.all()
        self._response.set_data(json.dumps([dict(c) for c in categories]))

    def create(self, name, price, image, available_date, stock):
        date_object = datetime.strptime(available_date, '%Y-%m-%d')
        product = Product(name=name, price=price, image=image, available_date=date_object)
        product_stock = ProductStock(available=(stock if stock else 1))
        product.stock = product_stock
        self._database.session.add(product)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(product)))

    def update(self, id, name=None, price=None, image=None, available_date=None, stock=None):
        product = Product.query.filter_by(id=id).first()
        if not product:
            raise ResourceNotFoundError()
        if product:
            product.name = name if name else product.name
            product.price = price if price else product.price
            product.image = image if image else product.image
            product.available_date = \
              datetime.strptime(available_date, '%Y-%m-%d')\
              if available_date\
              else product.available_date
            product_stock = ProductStock(available=(stock if stock else 1))
            product.stock = product_stock
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(product)))
        

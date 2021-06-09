from flask import Response
import json
from api.db.database import db
from api.db.models.product import Product
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

    def create(self, name, price, image, available_date):
        product = Product(name=name, price=price, image=image, available_date=available_date)
        self._database.session.add(product)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(product)))

    def update(self, id, name=None, price=None, image=None, available_date=None):
        product = Product.query.filter_by(id=id).first()
        if not product:
            raise ResourceNotFoundError()
        if product:
            product.name = name
            product.price = price
            product.image = image
            product.available_date = available_date
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(product)))
        

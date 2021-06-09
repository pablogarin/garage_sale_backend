from datetime import datetime
from flask import Response
import json
from api.db.database import db
from api.db.models.cart import Cart
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError


class CartResource(Resource):
    _id_key = "cart_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, id):
        cart = Cart.query.filter_by(id=id).first()
        if not cart:
            raise ResourceNotFoundError()
        self._response.set_data(json.dumps(dict(cart)))

    def get_all(self):
        categories = Cart.query.all()
        self._response.set_data(json.dumps([dict(c) for c in categories]))

    def create(self, total, products):
        date_object = datetime.now()
        cart = Cart(total=total, date=date_object, products=products)
        self._database.session.add(cart)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(cart)))

    def update(self, id, total=None, finished=None, date=None, products=None):
        cart = Cart.query.filter_by(id=id).first()
        if not cart:
            raise ResourceNotFoundError()
        if cart:
            cart.total = total if total else cart.total
            cart.finished = finished if finished else cart.finished
            cart.products = products if products else cart.products
            cart.date = \
              datetime.strptime(date, '%Y-%m-%d')\
              if date\
              else cart.date
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(cart)))
        

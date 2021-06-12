from flask import Response
import json
import re
from api.db.database import db
from api.db.models.order import Order
from api.db.models.user import User
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError
from api.utils.authentication import authenticate


class UserResource(Resource):
    _id_key = "user_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ResourceNotFoundError()
        if re.search(r"/user/\d+/orders", self._request.path):
            orders = Order.query.filter_by(user=user.id).all()
            self._response.set_data(json.dumps([dict(o) for o in orders]))
        elif re.search(r"/user/\d+/address", self._request.path):
            self._response.set_data(
                json.dumps([dict(a) for a in user.addresses]))
        else:
            self._response.set_data(json.dumps(dict(user)))

    def get_all(self):
        authenticate(self._request)
        users = User.query.all()
        self._response.set_data(json.dumps([dict(c) for c in users]))

    def create(self, first_name=None, last_name=None, email=None, phone=None):
        user = User(first_name=first_name, last_name=last_name, email=email, phone=phone)
        self._database.session.add(user)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(user)))

    def update(self, id, first_name=None, last_name=None, email=None, phone=None):
        user = User.query.filter_by(id=id).first()
        if not user:
            raise ResourceNotFoundError()
        if user:
            user.first_name = first_name if first_name else user.first_name
            user.last_name = last_name if last_name else user.last_name
            user.email = email if email else user.email
            user.phone = phone if phone else user.phone
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(user)))
        

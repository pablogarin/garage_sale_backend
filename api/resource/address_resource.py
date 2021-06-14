from flask import Response
import json
from api.db.models.user import User
from api.db.models.user import UserAddress
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError


class AddressResource(Resource):
    _id_key = "address_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, address_id, user_id=None):
        address = UserAddress.query.filter_by(id=address_id).first()
        if not address:
            raise ResourceNotFoundError()
        self._response.set_data(json.dumps(dict(address)))

    def get_all(self, user_id):
        categories = UserAddress.query.all()
        self._response.set_data(json.dumps([dict(c) for c in categories]))

    def create(self, name):
        address = UserAddress(name=name)
        self._database.session.add(address)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(address)))

    def update(self, address_id=None, user_id=None, name=None, products=[]):
        address = UserAddress.query.filter_by(id=address_id).first()
        if not address:
            raise ResourceNotFoundError()
        if address:
            address.name = name if name else address.name
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(address)))
        

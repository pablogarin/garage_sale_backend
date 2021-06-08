from flask import Response
import json
from api.db.database import db
from api.db.models.category import Category
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError


class CategoryResource(Resource):
    _id_key = "category_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, id):
        category = Category.query.filter_by(id=id).first()
        if not category:
            raise ResourceNotFoundError()
        self._response.set_data(json.dumps(dict(category)))

    def get_all(self):
        categories = Category.query.all()
        self._response.set_data(json.dumps([dict(c) for c in categories]))

    def create(self, name):
        category = Category(name=name)
        self._database.session.add(category)
        self._database.session.commit()
        self._response.set_data(json.dumps(dict(category)))

    def update(self, id, name):
        category = Category.query.filter_by(id=id).first()
        if not category:
            raise ResourceNotFoundError()
        if category:
            category.name = name
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(category)))
        

from flask import Flask
from flask import request
from flask import Response
from flask_cors import CORS
import json
import os

from api.db.database import db
from api.db.database import init_database
from api.middleware.auth_middleware import auth_middleware
from api.resource.resource import middleware
from api.resource.address_resource import AddressResource
from api.resource.cart_resource import CartResource
from api.resource.category_resource import CategoryResource
from api.resource.order_resource import OrderResource
from api.resource.product_resource import ProductResource
from api.resource.user_resource import UserResource
from api.db.models.user import UserAddress
from api.db.models.user import User
from api.db.models.order import Order
from api.utils.authentication import login
from api.utils.authentication import check_token
from api.utils.uploader import upload_files


def create_flask_app():
    app = Flask(__name__)
    CORS(app)
    database_uri = os.getenv("DATABASE", "sqlite:///database.db")
    print(database_uri)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    init_database(app)

    @app.route("/", methods=["GET"])
    def home():
        return "UP"
    
    @app.route("/carts", methods=["GET", "POST"])
    @app.route("/carts/<cart_id>", methods=["GET", "PUT", "DELETE"])
    def cart(*args, **kwargs):
        resource = CartResource(db)
        return resource.process_request(request, *args, **kwargs)

    @app.route("/categories", methods=["GET", "POST"])
    @app.route("/categories/<category_id>", methods=["GET", "PUT", "DELETE"])
    @middleware(request, callable=auth_middleware, methods=["POST", "PUT", "DELETE"])
    def category(*args, **kwargs):
        resource = CategoryResource(db)
        return resource.process_request(request, *args, **kwargs)
    
    @app.route("/orders", methods=["GET", "POST"])
    @app.route("/orders/<order_id>", methods=["GET", "PUT", "DELETE"])
    def order(*args, **kwargs):
        resource = OrderResource(db)
        return resource.process_request(request, *args, **kwargs)
    
    @app.route("/products", methods=["GET", "POST"])
    @app.route("/products/<product_id>", methods=["GET", "PUT", "DELETE"])
    @middleware(request, callable=auth_middleware, methods=["POST", "PUT", "DELETE"])
    def product(*args, **kwargs):
        resource = ProductResource(db)
        return resource.process_request(request, *args, **kwargs)
    
    @app.route("/users", methods=["GET", "POST"])
    @app.route("/users/<user_id>", methods=["GET", "PUT", "DELETE"])
    @app.route("/users/<user_id>/orders", methods=["GET"])
    def user(*args, **kwargs):
        resource = UserResource(db)
        return resource.process_request(request, *args, **kwargs)
    
    @app.route("/users/<user_id>/addresses", methods=["GET", "POST"])
    @app.route("/users/<user_id>/addresses/<address_id>", methods=["GET", "PUT", "DELETE"])
    def address(*args, **kwargs):
        resource = AddressResource(db)
        return resource.process_request(request, *args, **kwargs)
    
    @app.route("/files", methods=["POST"])
    def files():
      response = Response()
      response.headers["Content-type"] = "application/json"
      response.headers["Access-Control-Allow-Origin"] = "*"
      try:
        response.status_code = 200
        response.set_data(json.dumps({"files": upload_files(request)}))
      except Exception as e:
        response.status_code = 500
        response.set_data(json.dumps({"error": f"{e}"}))
      return response

    @app.route("/authenticate", methods=["POST"])
    def authenticate(*args, **kwargs):
        resp = Response()
        resp.headers["Content-type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.status_code = 200
        payload = request.json
        try:
            resp.set_data(json.dumps({"token": login(**payload)}))
        except Exception as e:
            resp.status_code = 403
            resp.set_data(json.dumps({"message": f"{e}"}))
        return resp
    @app.route("/validate-token", methods=["POST"])
    def validate_token(*args, **kwargs):
        resp = Response()
        resp.headers["Content-type"] = "application/json"
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.status_code = 200
        payload = request.json
        try:
            resp.set_data(json.dumps({"valid": check_token(**payload)}))
        except Exception as e:
            resp.status_code = 403
            resp.set_data(json.dumps({"message": f"{e}"}))
        return resp
    return app
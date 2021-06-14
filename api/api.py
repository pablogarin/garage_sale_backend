from flask import Flask
from flask import request
from flask_cors import CORS
import json

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


def create_flask_app():
  app = Flask(__name__)
  CORS(app)
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
  init_database(app)

  @app.route("/", methods=["GET"])
  def home():
    return "UP"
  
  @app.route("/cart", methods=["GET", "POST"])
  @app.route("/cart/<cart_id>", methods=["GET", "PUT", "DELETE"])
  def cart(*args, **kwargs):
    resource = CartResource(db)
    return resource.process_request(request, *args, **kwargs)

  @app.route("/category", methods=["GET", "POST"])
  @app.route("/category/<category_id>", methods=["GET", "PUT", "DELETE"])
  @middleware(request, callable=auth_middleware, methods=["POST", "PUT", "DELETE"])
  def category(*args, **kwargs):
    resource = CategoryResource(db)
    return resource.process_request(request, *args, **kwargs)
  
  @app.route("/order", methods=["GET", "POST"])
  @app.route("/order/<order_id>", methods=["GET", "PUT", "DELETE"])
  def order(*args, **kwargs):
    resource = OrderResource(db)
    return resource.process_request(request, *args, **kwargs)
  
  @app.route("/product", methods=["GET", "POST"])
  @app.route("/product/<product_id>", methods=["GET", "PUT", "DELETE"])
  @middleware(request, callable=auth_middleware, methods=["POST", "PUT", "DELETE"])
  def product(*args, **kwargs):
    resource = ProductResource(db)
    return resource.process_request(request, *args, **kwargs)
  
  @app.route("/user", methods=["GET", "POST"])
  @app.route("/user/<user_id>", methods=["GET", "PUT", "DELETE"])
  @app.route("/user/<user_id>/orders", methods=["GET"])
  def user(*args, **kwargs):
    resource = UserResource(db)
    return resource.process_request(request, *args, **kwargs)
  
  @app.route("/user/<user_id>/address", methods=["GET", "POST"])
  @app.route("/user/<user_id>/address/<address_id>", methods=["GET", "PUT", "DELETE"])
  def address(*args, **kwargs):
    resource = AddressResource(db)
    return resource.process_request(request, *args, **kwargs)
  
  return app
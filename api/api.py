from flask import Flask
from flask import request
from flask_cors import CORS
import json

from api.db.database import db
from api.db.database import init_database
from api.middleware.auth_middleware import auth_middleware
from api.resource.resource import middleware
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
  def cart(cart_id=None):
    resource = CartResource(db)
    return resource.process_request(request, cart_id=cart_id)

  @app.route("/category", methods=["GET", "POST"])
  @app.route("/category/<category_id>", methods=["GET", "PUT", "DELETE"])
  @middleware(request, callable=auth_middleware, methods=["POST", "PUT", "DELETE"])
  def category(category_id=None):
    resource = CategoryResource(db)
    return resource.process_request(request, category_id=category_id)
  
  @app.route("/order", methods=["GET", "POST"])
  @app.route("/order/<order_id>", methods=["GET", "PUT", "DELETE"])
  def order(order_id=None):
    resource = OrderResource(db)
    return resource.process_request(request, order_id=order_id)
  
  @app.route("/product", methods=["GET", "POST"])
  @app.route("/product/<product_id>", methods=["GET", "PUT", "DELETE"])
  @middleware(request, callable=auth_middleware, methods=["POST", "PUT", "DELETE"])
  def product(product_id=None):
    resource = ProductResource(db)
    return resource.process_request(request, product_id=product_id)
  
  @app.route("/user", methods=["GET", "POST"])
  @app.route("/user/<user_id>", methods=["GET", "PUT", "DELETE"])
  @app.route("/user/<user_id>/orders", methods=["GET"])
  @app.route("/user/<user_id>/address", methods=["GET", "POST", "PUT"])
  def user(user_id=None):
    resource = UserResource(db)
    return resource.process_request(request, user_id=user_id)
  
  return app
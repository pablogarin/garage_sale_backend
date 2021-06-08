from flask import Flask
from flask import request
from flask_cors import CORS
import json

from api.db.database import db
from api.db.database import init_database
from api.resource.category_resource import CategoryResource


def create_flask_app():
  app = Flask(__name__)
  CORS(app)
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
  init_database(app)

  @app.route("/", methods=["GET"])
  def home():
    return "UP"
  
  @app.route("/category", methods=["GET", "POST"])
  @app.route("/category/<category_id>", methods=["GET", "PUT", "DELETE"])
  def category(category_id=None):
    resource = CategoryResource(db)
    return resource.process_request(request, category_id=category_id)
  return app
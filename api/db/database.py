from flask_sqlalchemy import SQLAlchemy
database_uri = "sqlite:///database.db"

db = SQLAlchemy()

def init_database(app):
    db.init_app(app)


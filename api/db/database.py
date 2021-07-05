from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_database(app):
    db.init_app(app)


from api.db.database import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    available_date = db.Column(db.DateTime, nullable=False)

    def __iter__(self):
        data = {
            "id": self.id,
            "name": self.name
        }
        for key, value in data.items():
            yield key, value

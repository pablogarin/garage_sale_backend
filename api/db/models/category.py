from api.db.database import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __iter__(self):
        data = {
            "id": self.id,
            "name": self.name
        }
        for key, value in data.items():
            yield key, value

from sqlalchemy.orm import lazyload
from api.db.database import db


class UserAddress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    address_line_1 = db.Column(db.String(200), nullable=False)
    address_line_2 = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(200), nullable=False)
    postal_code = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(200), nullable=False)

    def __iter__(self):
        data = {
            "id": self.id,
            "addressLine_1": self.address_line_1,
            "addressLine_2": self.address_line_2,
            "city": self.city,
            "state": self.state,
            "postalCode": self.postal_code,
            "country": self.country
        }
        for key, value in data.items():
            yield key, value


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    addresses = db.relationship("UserAddress", lazy="subquery")

    def __iter__(self):
        data = {
            "id": self.id,
            "firstName": self.first_name,
            "lastName": self.last_name,
            "email": self.email,
            "phone": self.phone
        }
        for key, value in data.items():
            yield key, value

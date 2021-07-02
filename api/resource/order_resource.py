from api.resource.invalid_request_error import InvalidRequestError
from datetime import datetime
from flask import Response
import json
from api.db.database import db
from api.db.models.order import Order
from api.db.models.order import OrderProduct
from api.db.models.product import Product
from api.db.models.user import User
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError
from api.utils.authentication import authenticate
from api.utils.user_utils import check_email


class OrderResource(Resource):
    _id_key = "order_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, order_id=None):
        order = Order.query.filter_by(id=order_id).first()
        if not order:
            raise ResourceNotFoundError()
        order_dict = dict(order)
        order_dict["user"] = dict(order.user_resource)
        self._response.set_data(json.dumps(order_dict))

    def get_all(self):
        authenticate(self._request)
        filters = self._get_filters()
        if not filters:
            orders = Order.query.all()
            self._response.set_data(json.dumps([
                {**dict(c), "user": dict(c.user_resource)} for c in orders]))
        else:
            orders = Order.query.filter_by(**filters)
            self._response.set_data(json.dumps([dict(c) for c in orders]))

    def create(self, email=None, products=None):
        if not email:
            raise InvalidRequestError("You must provide a valid e-mail")
        if not check_email(email):
            raise InvalidRequestError("You must provide a valid e-mail")
        user = User.query.filter_by(email=email).first()
        if not user:
            raise InvalidRequestError("User is not registered")
        date_object = datetime.now()
        order = Order(total=0.0, date=date_object, products=self._get_products(products), user=user.id)
        order.total = self._get_total(order)
        self._discount_stock(order.products)
        self._database.session.add(order)
        self._database.session.commit()
        self._response.set_data(json.dumps({**dict(order)}))
    
    def _get_products(self, product_list, order=None):
        products = list()
        for prd in product_list:
            deleted = False
            if "id" in prd:
                product = Product.query.filter_by(id=prd["id"]).first()
                order_product = None
                if order:
                    order_product = OrderProduct.query.filter_by(order_id=order.id, product_id=product.id).first()
                    if prd["quantity"] <= 0:
                        deleted = True
                        self._database.session.delete(order_product)
                        continue
                    elif order_product:
                        order_product.quantity = prd["quantity"]
                if not deleted and order_product is None:
                    order_product = OrderProduct(quantity=prd["quantity"], price=product.price, total_discount=0.0, product=product)
                if order_product.quantity > product.stock.available:
                    raise Exception("Not enough stock")
                products.append(order_product)
            else:
                raise InvalidRequestError("Product list is malformed")
        if order:
            products.extend(order.products)
        return products
    
    def _discount_stock(self, products):
        for prd in products:
            stock = prd.product.stock
            available = stock.available - stock.reserved
            if available >= prd.quantity:
                stock.reserved = prd.quantity
                self._database.session.add(prd.product.stock)
            else:
                raise Exception('No enough stock')

    def _get_total(self, order):
        total = 0.0
        for product in order.products:
            total += product.price * product.quantity
        return total

    def update(self, id, total=None, status=None, date=None, products=None):
        order = Order.query.filter_by(id=id).first()
        if not order:
            raise ResourceNotFoundError()
        if order:
            order.total = total if total else order.total
            order.status = status if status else order.status
            order.products = self._get_products(products, order=order) if products else order.products
            order.date = \
              datetime.strptime(date, '%Y-%m-%d')\
              if date\
              else order.date
            order.total = self._get_total(order)
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(order)))
    
    def _get_filters(self):
        filters = dict()
        allowed_fields = ["status", "date"]
        for field in allowed_fields:
            value = self._request.args.get(field)
            if value is not None:
                filters[field] = value
        return filters

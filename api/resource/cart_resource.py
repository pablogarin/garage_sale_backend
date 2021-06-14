from api.utils.authentication import authenticate
from api.resource.invalid_request_error import InvalidRequestError
from datetime import datetime
from flask import Response
import json
from api.db.database import db
from api.db.models.cart import Cart
from api.db.models.cart import CartProduct
from api.db.models.product import Product
from api.resource.resource import Resource
from api.resource.resource_not_found_error import ResourceNotFoundError
from api.utils.authentication import authenticate


class CartResource(Resource):
    _id_key = "cart_id"

    @property
    def id_key(self):
        return self._id_key

    def __init__(self, database):
        self._response = Response()
        self._response.headers["Content-type"] = "application/json"
        self._database = database
    
    def get(self, cart_id=None):
        cart = Cart.query.filter_by(id=cart_id).first()
        if not cart:
            raise ResourceNotFoundError()
        self._response.set_data(json.dumps(dict(cart)))

    def get_all(self):
        authenticate(self._request)
        carts = Cart.query.all()
        self._response.set_data(json.dumps([dict(c) for c in carts]))

    def create(self, products=None, total=None):
        date_object = datetime.now()
        cart = Cart(total=0.0, date=date_object, products=self._get_products(products))
        cart.total = self._get_total(cart)
        self._database.session.add(cart)
        self._database.session.commit()
        self._response.set_data(json.dumps({**dict(cart)}))
    
    def _get_products(self, product_list, cart=None):
        products = list()
        for prd in product_list:
            deleted = False
            if "id" in prd:
                product = Product.query.filter_by(id=prd["id"]).first()
                cart_product = None
                if cart:
                    cart_product = CartProduct.query.filter_by(cart_id=cart.id, product_id=product.id).first()
                    if prd["quantity"] <= 0:
                        deleted = True
                        self._database.session.delete(cart_product)
                        continue
                    elif cart_product:
                        cart_product.quantity = prd["quantity"]
                if not deleted and cart_product is None:
                    cart_product = CartProduct(quantity=prd["quantity"], price=product.price, total_discount=0.0, product=product)
                if cart_product.quantity > product.stock.available:
                    raise Exception("Not enough stock")
                products.append(cart_product)
            else:
                raise InvalidRequestError("Product list is malformed")
        if cart:
            products.extend(cart.products)
        return products
    
    def _get_total(self, cart):
        total = 0.0
        for product in cart.products:
            total += product.price * product.quantity
        return total

    def update(self, cart_id=None, total=None, finished=None, date=None, products=None):
        cart = Cart.query.filter_by(id=cart_id).first()
        if not cart:
            raise ResourceNotFoundError()
        if cart:
            cart.finished = finished if finished else cart.finished
            cart.products = self._get_products(products, cart=cart) if products else cart.products
            cart.date = \
              datetime.strptime(date, '%Y-%m-%d')\
              if date\
              else cart.date
            cart.total = self._get_total(cart)
            self._database.session.commit()
            self._response.set_data(json.dumps(dict(cart)))
        

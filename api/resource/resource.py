from abc import ABC
from abc import abstractmethod
from flask import Response
import json
from api.resource.invalid_request_error import InvalidRequestError
from api.resource.resource_not_found_error import ResourceNotFoundError


def middleware(request, callable=None, methods=None):
    def apply(func):
        def wrapper(*args, **kwargs):
            try:
                callable(request, *args, methods=methods, **kwargs)
                return func(*args, **kwargs)
            except Exception as e:
                resp = Response()
                resp.headers["Content-type"] = "application/json"
                resp.status_code = e.status_code if hasattr(e, "status_code") else 500
                resp.set_data(json.dumps({"message": f"{e}"}))
                return resp
        wrapper.__name__ = func.__name__
        return wrapper
    return apply


class Resource(ABC):
    @property
    @abstractmethod
    def id_key(self):
        return self._id_key
    
    @abstractmethod
    def get(self, id, *args, **kwargs):
      pass
    
    @abstractmethod
    def get_all(self, *args, **kwargs):
      pass

    @abstractmethod
    def create(self, *args, **kwargs):
      pass

    @abstractmethod
    def update(self, id, *args, **kwargs):
      pass

    def process_request(self, *args, **kwargs):
        request, *_ = args
        self._request = request
        try:
            if self._request.method == "GET":
                if self.id_key in kwargs:
                    self.get(**kwargs)
                else:
                    self.get_all()
            elif self._request.method == "POST":
                payload = self._request.json
                if payload is None:
                    raise InvalidRequestError("Invalid data")
                self.create(**payload)
            elif self._request.method == "PUT":
                payload = self._request.json
                if self.id_key not in kwargs:
                    raise InvalidRequestError("No id provided")
                self.update(**payload, **kwargs)
        except InvalidRequestError as e:
            self._response.status_code = 422
            self._response.set_data(json.dumps({"success": False, "error": f"{e}"}))
        except ResourceNotFoundError as e:
            self._response.status_code = 404
            self._response.set_data(json.dumps({"success": False, "error": "Resource not found"}))
        except Exception as e:
            self._response.status_code = 500
            self._response.set_data(json.dumps({"success": False, "error": f"{e}"}))
        return self._response
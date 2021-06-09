from abc import ABC
from abc import abstractmethod
import json
from api.resource.invalid_request_error import InvalidRequestError
from api.resource.resource_not_found_error import ResourceNotFoundError


class Resource(ABC):
    @property
    @abstractmethod
    def id_key(self):
        return self._id_key

    def process_request(self, *args, **kwargs):
        request, *_ = args
        try:
            if request.method == "GET":
                if kwargs[self.id_key]:
                    self.get(kwargs[self.id_key])
                else:
                    self.get_all()
            elif request.method == "POST":
                payload = request.json
                if payload is None:
                    raise InvalidRequestError("Invalid data")
                self.create(**payload)
            elif request.method == "PUT":
                payload = request.json
                if not kwargs[self.id_key]:
                    raise InvalidRequestError("No id provided")
                self.update(kwargs[self.id_key], **payload)
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
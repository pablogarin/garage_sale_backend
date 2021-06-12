from api.utils.authentication import authenticate


def auth_middleware(request, *args, methods=["POST", "PUT", "DELETE"], **kwargs):
    if request.method in methods:
        authenticate(request)
    
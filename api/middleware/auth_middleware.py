from api.utils.authentication import authenticate


def auth_middleware(request, methods=["POST", "PUT", "DELETE"]):
    if request.method in methods:
        authenticate(request)
    
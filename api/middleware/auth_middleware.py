import base64
import dotenv
import os
import re


dotenv.load_dotenv()


class NotAuthorizedError(Exception):
    status_code = 403


def auth_middleware(request, *args, methods=["POST", "PUT", "DELETE"], **kwargs):
    admin_user = os.getenv("ADMIN")
    admin_passwd = os.getenv("ADMIN_PASSWD")
    if not admin_user or not admin_passwd:
        raise Exception("You must config admin username and password in environment")
    if request.method in methods:
        if request.headers["Authorization"]:
            try:
                auth_hash = re.search(r"^Basic (.*)$", request.headers["Authorization"]).group(1)
                auth_string = base64.b64decode(auth_hash).decode("utf-8") 
                user, password = auth_string.split(":")
                if user != admin_user or password != admin_passwd:
                    raise NotAuthorizedError("Wrong credentials")
            except:
                raise NotAuthorizedError("Wrong credentials")
        else:
            raise NotAuthorizedError("Wrong credentials")
    
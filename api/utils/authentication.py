import base64
import dotenv
import json
import os
import re
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from jwt import (
    JWT,
    jwk_from_dict,
    jwk_from_pem,
)
from jwt.utils import get_int_from_datetime


dotenv.load_dotenv()


class NotAuthorizedError(Exception):
    status_code = 403


def generate_jwt():
    instance = JWT()
    private_key = os.getenv("PRIVATE_KEY")
    message = {
        "iss": "pablogarin.dev",
        "user": "admin",
        "permissions": [
            "create",
            "edit",
            "delete"
        ],
        "iat": get_int_from_datetime(datetime.now(timezone.utc)),
        "exp": get_int_from_datetime(
            datetime.now(timezone.utc) + timedelta(hours=1)),
    }
    with open(private_key, 'rb') as fh:
        signing_key = jwk_from_pem(fh.read())
        compact_jws = instance.encode(message, signing_key, alg='RS256')
        return compact_jws


def login(user, passwd):
    admin_user = os.getenv("ADMIN")
    admin_passwd = os.getenv("ADMIN_PASSWD")
    if user == admin_user and passwd == admin_passwd:
        return generate_jwt()
    raise Exception('Invalid credentials')

def check_token(token):
    instance = JWT()
    public_key = os.getenv("PUBLIC_KEY")
    try:
        with open(f"{public_key}", 'rb') as fh:
            verifying_key = jwk_from_pem(fh.read())
        compact_jws = instance.decode(f"{token}", verifying_key, do_time_check=True)
        if compact_jws["iss"] != "pablogarin.dev":
            raise NotAuthorizedError("Wrong credentials")
        if compact_jws["user"] != "admin":
            raise NotAuthorizedError("Wrong credentials")
    except Exception as e:
        print(e)
        raise NotAuthorizedError("Wrong credentials")
    return True


def authenticate(request):
    admin_user = os.getenv("ADMIN")
    admin_passwd = os.getenv("ADMIN_PASSWD")
    if not admin_user or not admin_passwd:
        raise Exception("You must config admin username and password in environment")
    if request.headers["Authorization"]:
        try:
            auth_hash = re.search(r"^Bearer (.*)$", request.headers["Authorization"]).group(1)
            if check_token(auth_hash):
                return True
        except:
            raise NotAuthorizedError("Wrong credentials")
    else:
        raise NotAuthorizedError("Wrong credentials")
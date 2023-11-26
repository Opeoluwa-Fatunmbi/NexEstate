from django.conf import settings  # import the settings file
from apps.accounts.models import *  # import the Jwt model
from datetime import datetime, timedelta  # import datetime and timedelta
import jwt, random, string  # import jwt, random and string

ALGORITHM = "HS256"  # set algorithm to HS256


class Authentication:  # create Authentication class
    # generate random string
    def get_random(length: int):
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    # generate access token based and encode user's id
    def create_access_token(payload: dict):
        expire = datetime.utcnow() + timedelta(
            minutes=int(settings.ACCESS_TOKEN_LIFETIME_MINUTES)
        )
        to_encode = {"exp": expire, **payload}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # generate random refresh token
    def create_refresh_token(
        expire=datetime.utcnow()
        + timedelta(minutes=int(settings.REFRESH_TOKEN_LIFETIME_MINUTES)),
    ):
        return jwt.encode(
            {"exp": expire, "data": Authentication.get_random(10)},
            settings.SECRET_KEY,
            algorithm=ALGORITHM,
        )

    # decode access token from header
    def decode_jwt(token: str):
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        except:
            decoded = False
        return decoded

    # decode refresh token from cookie
    def decodeAuthorization(token: str):
        decoded = Authentication.decode_jwt(token[7:])
        if not decoded:
            return None
        jwt_obj = (
            Jwt.objects.filter(user_id=decoded["user_id"])
            .select_related("user", "user__avatar")
            .first()
        )
        if not jwt_obj:
            return None
        return jwt_obj.user

    # Blacklist refresh token
    def blacklist_token(token: str):
        decoded = Authentication.decode_jwt(token)
        if not decoded:
            return None
        jwt_obj = Jwt.objects.filter(user_id=decoded["user_id"]).first()
        if not jwt_obj:
            return None
        jwt_obj.blacklisted = True
        jwt_obj.save()
        return True

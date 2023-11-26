from django.utils import timezone
from rest_framework.permissions import BasePermission
from apps.accounts.auth import Authentication
from apps.accounts.models import User, Jwt
from apps.common.models import File, GuestUser
from apps.common.exceptions import RequestError
from datetime import timedelta
from uuid import UUID


class IsAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        if not http_auth:
            raise RequestError(err_msg="Auth Bearer not provided!", status_code=401)
        user = Authentication.decodeAuthorization(http_auth)
        if not user:
            raise RequestError(
                err_msg="Auth Token is Invalid or Expired!", status_code=401
            )
        request.user = user
        if request.user and request.user.is_authenticated:
            return True
        return False


class IsGuestOrAuthenticatedCustom(BasePermission):
    def has_permission(self, request, view):
        http_auth = request.META.get("HTTP_AUTHORIZATION")
        guest_id = request.headers.get("Guestuserid")
        if http_auth:
            user = Authentication.decodeAuthorization(http_auth)
            if not user:
                raise RequestError(
                    err_msg="Auth Token is Invalid or Expired!", status_code=401
                )
            request.user = user
        elif guest_id:
            guest = GuestUser.objects.filter(id=guest_id)
            if guest.exists():
                request.user = guest.get()
            else:
                request.user = None
        else:
            request.user = None
        return True


def is_uuid(value):
    try:
        return str(UUID(value))
    except:
        return None


def is_int(value):
    if not value:
        return None
    try:
        return int(value)
    except:
        raise RequestError(err_msg="Invalid Quantity params", status_code=422)


# Test Utils
class TestUtil:
    def new_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Name",
            "email": "test@example.com",
        }
        user = User(**user_dict)
        user.set_password("testpassword")
        user.save()
        return user

    def verified_user():
        user_dict = {
            "first_name": "Test",
            "last_name": "Verified",
            "email": "testverifieduser@example.com",
            "is_email_verified": True,
        }
        user = User(**user_dict)
        user.set_password("testpassword")
        user.save()
        return user

    def another_verified_user():
        create_user_dict = {
            "first_name": "AnotherTest",
            "last_name": "UserVerified",
            "email": "anothertestverifieduser@example.com",
            "is_email_verified": True,
        }
        user = User(**create_user_dict)
        user.set_password("anothertestverifieduser123")
        user.save()
        return user

    def auth_token(verified_user):
        access = Authentication.create_access_token({"user_id": str(verified_user.id)})
        refresh = Authentication.create_refresh_token()
        Jwt.objects.create(user_id=verified_user.id, access=access, refresh=refresh)
        return access

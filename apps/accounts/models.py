from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import UserManager
from django.conf import settings
from django.utils import timezone
from apps.common.models import BaseModel

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        default=uuid.uuid4, primary_key=True, unique=True, editable=False
    )
    first_name = models.CharField(_("first_name"), max_length=50)
    last_name = models.CharField(_("last_name"), max_length=50)
    email = models.EmailField(_("Email_address"), unique=True)
    is_staff = models.BooleanField(_("staff_status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)
    is_superuser = models.BooleanField(_("superuser_status"), default=False)
    is_email_verified = models.BooleanField(_("email_verified"), default=False)
    terms_agreement = models.BooleanField(_("terms_agreement"), default=False)
    avatar = models.ImageField(upload_to="avatars/", null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Jwt(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    blacklisted = models.BooleanField(default=False)


class Otp(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()

    objects = UserManager()

    def check_expiration(self):
        now = timezone.now()
        diff = now - self.updated_at
        if diff.total_seconds() > int(settings.EMAIL_OTP_EXPIRE_SECONDS):
            return True
        return False

    def __str__(self):
        return f"{self.user.full_name} - {self.code}"

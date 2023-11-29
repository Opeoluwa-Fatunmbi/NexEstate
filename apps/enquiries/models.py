from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from apps.common.models import BaseModel
from autoslug import AutoSlugField as Auto


class Enquiry(BaseModel):
    name = models.CharField(_("Your Name"), max_length=100)
    slug = Auto(populate_from="name", unique=True)
    phone_number = PhoneNumberField(
        _("Phone number"), max_length=30, default="+254703229589"
    )
    email = models.EmailField(_("Email"))
    subject = models.CharField(_("Subject"), max_length=100)
    message = models.TextField(_("Message"))
    is_answered = models.BooleanField(_("Is answered"), default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Enquiries"

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.common.models import BaseModel
from apps.accounts.models import User
from apps.properties.managers import PropertyPublishedManager


class Payment(BaseModel):
    class PaymentStatus(models.TextChoices):
        PENDING = "Pending", _("Pending")
        PAID = "Paid", _("Paid")
        FAILED = "Failed", _("Failed")

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="payments",
        on_delete=models.DO_NOTHING,
    )
    product_name = models.CharField(
        verbose_name=_("Product Name"), max_length=255, default="Product Name"
    )
    product_image = models.URLField(
        verbose_name=_("Product Image"),
        max_length=255,
        default="https://via.placeholder.com/150",
    )
    amount = models.IntegerField(
        verbose_name=_("Amount"),
        default=100,
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
    )
    session_id = models.CharField(
        verbose_name=_("Session ID"),
        max_length=255,
        blank=True,
        null=True,
    )
    reference = models.CharField(
        verbose_name=_("Reference"),
        max_length=255,
        blank=True,
        null=True,
    )
    transaction_id = models.CharField(
        verbose_name=_("Transaction ID"),
        max_length=255,
        blank=True,
        null=True,
    )
    transaction_date = models.DateTimeField(
        verbose_name=_("Transaction Date"),
        blank=True,
        null=True,
    )
    transaction_status = models.CharField(
        verbose_name=_("Transaction Status"),
        max_length=255,
        blank=True,
        null=True,
    )
    transaction_reference = models.CharField(
        verbose_name=_("Transaction Reference"),
        max_length=255,
        blank=True,
        null=True,
    )
    transaction_message = models.CharField(
        verbose_name=_("Transaction Message"),
        max_length=255,
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(verbose_name=_("Quantity"), default=1)

    objects = models.Manager()
    published = PropertyPublishedManager()

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

    def __str__(self):
        return self.product_name

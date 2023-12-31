from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

# from apps.ratings.models import Rating

from apps.common.models import BaseModel

User = get_user_model()


class Profile(BaseModel):
    class Gender(models.TextChoices):
        MALE = "Male", _("Male")
        FEMALE = "Female", _("Female")
        OTHER = "Other", _("Other")

    class Salary(models.TextChoices):
        LOW = "Low", _("Low")
        MEDIUM = "Medium", _("Medium")
        HIGH = "High", _("High")

    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        verbose_name=_("Phone Number"), max_length=30, default="+25474204242"
    )
    about_me = models.TextField(
        verbose_name=_("About me"), default="say something about yourself"
    )
    license = models.CharField(
        verbose_name=_("Real Estate license"), max_length=20, blank=True, null=True
    )
    profile_photo = models.ImageField(
        verbose_name=_("Profile Photo"), default="/profile_default.png"
    )
    gender = models.CharField(
        verbose_name=_("Gender"),
        choices=Gender.choices,
        default=Gender.OTHER,
        max_length=20,
    )
    country = CountryField(
        verbose_name=_("Country"), default="NG", blank=False, null=False
    )
    city = models.CharField(
        verbose_name=_("City"),
        max_length=180,
        default="Nairobi",
        blank=False,
        null=False,
    )
    salary = models.CharField(
        verbose_name=_("Salary"),
        choices=Salary.choices,
        default=Salary.LOW,
        max_length=20,
    )
    is_buyer = models.BooleanField(
        verbose_name=_("Buyer"),
        default=False,
        help_text=_("Are you looking to Buy a Property?"),
    )
    is_seller = models.BooleanField(
        verbose_name=_("Seller"),
        default=False,
        help_text=_("Are you looking to sell a property?"),
    )
    is_agent = models.BooleanField(
        verbose_name=_("Agent"), default=False, help_text=_("Are you an agent?")
    )
    is_top_agent = models.BooleanField(verbose_name=_("Top Agent"), default=False)
    # rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    # rating = models.ForeignKey(Rating, on_delete=models.CASCADE, null=True, blank=True)
    num_reviews = models.IntegerField(
        verbose_name=_("Number of Reviews"), default=0, null=True, blank=True
    )
    num_properties = models.IntegerField(
        verbose_name=_("Number of Properties"), default=0, null=True, blank=True
    )
    num_sales = models.IntegerField(
        verbose_name=_("Number of Sales"), default=0, null=True, blank=True
    )
    num_purchases = models.IntegerField(
        verbose_name=_("Number of Purchases"), default=0, null=True, blank=True
    )
    num_rentals = models.IntegerField(
        verbose_name=_("Number of Rentals"), default=0, null=True, blank=True
    )

    def __str__(self):
        return f"{self.user.email}'s profile"

    # @property
    # def avg_rating(self):
    #     reviews = [review.rating for review in self.reviews.all()]
    #     avg = 0
    #     if len(reviews) > 0:
    #         avg = round(mean(list(reviews)))  # Mean
    #     return avg

    class Meta:
        app_label = "profiles"

import random
import string
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from apps.common.models import BaseModel
from apps.accounts.models import User
from apps.properties.managers import PropertyPublishedManager
from statistics import mean


class PropertyCategories(BaseModel):
    name = models.CharField(
        verbose_name=_("Category Name"), max_length=250, unique=True
    )
    slug = AutoSlugField(populate_from="name", unique=True, always_update=True)
    description = models.TextField(
        verbose_name=_("Category Description"),
        default="Default description",
    )
    image = models.ImageField(
        verbose_name=_("Category Image"), default="/house_sample.jpg"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Property Category"
        verbose_name_plural = "Property Categories"


class Property(BaseModel):
    class AdvertType(models.TextChoices):
        FOR_SALE = "For Sale", _("For Sale")
        FOR_RENT = "For Rent", _("For Rent")
        AUCTION = "Auction", _("Auction")

    class PropertyType(models.TextChoices):
        HOUSE = "House", _("House")
        APARTMENT = "Apartment", _("Apartment")
        OFFICE = "Office", _("Office")
        WAREHOUSE = "Warehouse", _("Warehouse")
        COMMERCIAL = "Commercial", _("Commercial")
        OTHER = "Other", _("Other")

    user = models.ForeignKey(
        User,
        verbose_name=_("Agent,Seller or Buyer"),
        related_name="agent_buyer",
        on_delete=models.DO_NOTHING,
    )

    title = models.CharField(verbose_name=_("Property Title"), max_length=250)
    slug = AutoSlugField(populate_from="title", unique=True, always_update=True)
    ref_code = models.CharField(
        verbose_name=_("Property Reference Code"),
        max_length=255,
        unique=True,
        blank=True,
    )
    description = models.TextField(
        verbose_name=_("Description"),
        default="Default description",
        unique=True,
    )
    country = CountryField(
        verbose_name=_("Country"),
        default="NG",
        blank_label="(select country)",
    )
    city = models.CharField(verbose_name=_("City"), max_length=180, default="Lagos")
    postal_code = models.CharField(
        verbose_name=_("Postal Code"), max_length=100, default="10123"
    )
    street_address = models.CharField(
        verbose_name=_("Street Address"), max_length=150, default="Allen Avenue"
    )
    property_number = models.IntegerField(
        verbose_name=_("Property Number"),
        validators=[MinValueValidator(1)],
        default=112,
    )
    price = models.DecimalField(
        verbose_name=_("Price"), max_digits=8, decimal_places=2, default=0.0
    )  # Cents(Stripe)
    tax = models.DecimalField(
        verbose_name=_("Property Tax"),
        max_digits=6,
        decimal_places=2,
        default=0.18,
        help_text="18% property tax charged",
    )
    plot_area = models.DecimalField(
        verbose_name=_("Plot Area(m^2)"), max_digits=8, decimal_places=2, default=0.0
    )
    total_floors = models.IntegerField(verbose_name=_("Number of floors"), default=0)
    bedrooms = models.IntegerField(verbose_name=_("Bedrooms"), default=1)
    bathrooms = models.DecimalField(
        verbose_name=_("Bathrooms"), max_digits=4, decimal_places=2, default=1.0
    )
    advert_type = models.CharField(
        verbose_name=_("Advert Type"),
        max_length=50,
        choices=AdvertType.choices,
        default=AdvertType.FOR_SALE,
    )
    zip_code = models.CharField(
        verbose_name=_("Zip Code"), max_length=100, default="10123"
    )
    parking = models.BooleanField(verbose_name=_("Parking"), default=False)
    furnished = models.BooleanField(verbose_name=_("Furnished"), default=False)
    property_type = models.CharField(
        verbose_name=_("Property Type"),
        max_length=50,
        choices=PropertyType.choices,
        default=PropertyType.OTHER,
    )

    cover_photo = models.ImageField(
        verbose_name=_("Main Photo"), default="/house_sample.jpg", null=True, blank=True
    )
    photo1 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo2 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo3 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    photo4 = models.ImageField(
        default="/interior_sample.jpg",
        null=True,
        blank=True,
    )
    published_status = models.BooleanField(
        verbose_name=_("Published Status"), default=False
    )
    views = models.IntegerField(verbose_name=_("Total Views"), default=0)
    session_id = models.CharField(
        verbose_name=_("Stripe Session ID"), max_length=255, blank=True, null=True
    )
    category = models.ForeignKey(
        PropertyCategories,
        verbose_name=_("Property Category"),
        related_name="property_category",
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    is_available = models.BooleanField(  # For Sale or For Rent
        verbose_name=_("Is Available"), default=True
    )
    is_featured = models.BooleanField(verbose_name=_("Is Featured"), default=False)
    is_published = models.BooleanField(verbose_name=_("Is Published"), default=False)
    is_sold = models.BooleanField(verbose_name=_("Is Sold"), default=False)
    is_rented = models.BooleanField(verbose_name=_("Is Rented"), default=False)
    is_occupied = models.BooleanField(verbose_name=_("Is Occupied"), default=False)
    is_new = models.BooleanField(verbose_name=_("Is New"), default=False)
    is_hot_deal = models.BooleanField(verbose_name=_("Is Hot Deal"), default=False)
    is_top_rated = models.BooleanField(verbose_name=_("Is Top Rated"), default=False)
    is_verified = models.BooleanField(verbose_name=_("Is Verified"), default=False)
    is_approved = models.BooleanField(verbose_name=_("Is Approved"), default=False)
    is_deleted = models.BooleanField(verbose_name=_("Is Deleted"), default=False)
    is_archived = models.BooleanField(verbose_name=_("Is Archived"), default=False)
    is_favorite = models.BooleanField(verbose_name=_("Is Favorite"), default=False)
    property_valuation_report = models.TextField(
        verbose_name=_("Property Valuation Report"),
        blank=True,
        null=True,
        help_text="Property valuation report",
    )
    objects = models.Manager()
    published = PropertyPublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def save(self, *args, **kwargs):
        self.title = str.title(self.title)
        self.description = str.capitalize(self.description)
        self.ref_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=10)
        )
        super(Property, self).save(*args, **kwargs)

    @property
    def final_property_price(self):
        tax_percentage = self.tax
        property_price = self.price
        tax_amount = round(tax_percentage * property_price, 2)
        price_after_tax = float(round(property_price + tax_amount, 2))
        return price_after_tax

    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ""
        return url


class PropertyViews(BaseModel):
    ip = models.CharField(verbose_name=_("IP Address"), max_length=250)
    property = models.ForeignKey(
        Property, related_name="property_views", on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"Total views on - {self.property.title} is - {self.property.views} view(s)"
        )

    class Meta:
        verbose_name = "Total Property View"
        verbose_name_plural = "Total Property Views"


# models.py
class FavouriteProperty(BaseModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="favorite_properties",
        on_delete=models.CASCADE,
    )
    property = models.ForeignKey(
        Property,
        verbose_name=_("Property"),
        related_name="favorited_by",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.email}'s Favorite: {self.property.title}"

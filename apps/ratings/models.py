from django.db import models
from apps.accounts.models import User
from apps.common.models import BaseModel
from apps.profiles.models import Profile
from django.utils.translation import gettext_lazy as _
from apps.properties.models import Property

# Create your models here.


class Rating(BaseModel):
    class Range(models.IntegerChoices):
        RATING_1 = 1, _("Poor")
        RATING_2 = 2, _("Fair")
        RATING_3 = 3, _("Good")
        RATING_4 = 4, _("Very Good")
        RATING_5 = 5, _("Excellent")

    user = models.ForeignKey(
        User,
        verbose_name=_("User providing the rating"),
        on_delete=models.SET_NULL,
        null=True,
    )

    # agent = models.ForeignKey(
    #    Profile,
    #    verbose_name=_("Agent being rated"),
    #    related_name="agent_review",
    #    on_delete=models.SET_NULL,
    #    null=True,
    # )

    rating = models.IntegerField(
        verbose_name=_("Rating"),
        choices=Range.choices,
        help_text="1=Poor, 2=Fair, 3=Good, 4=Very Good, 5=Excellent",
        default=0,
    )
    comment = models.TextField(verbose_name=_("Comment"))

    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")

    def __str__(self):
        return f"{self.agent} rated at {self.rating}"

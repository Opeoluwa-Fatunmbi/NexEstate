from django.contrib import admin
from .models import Rating

# Register your models here.


class RatingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "rating",
        "comment",
        "property",
    )
    list_filter = ("user", "rating", "property")
    search_fields = ("user", "rating", "property")


admin.site.register(Rating, RatingAdmin)

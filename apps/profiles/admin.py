from django.contrib import admin
from .models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "phone_number", "country", "city")
    list_filter = list_display
    search_fields = list_display
    list_per_page = 10


admin.site.register(Profile, ProfileAdmin)

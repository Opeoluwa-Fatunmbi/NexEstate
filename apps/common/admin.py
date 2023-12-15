from django.contrib import admin
from django.utils.safestring import mark_safe

# Register your models here.
admin.site.site_header = mark_safe(
    '<strong style="font-family: sans-serif; font-weight:bold; color: #ffffff; font-size: 20px;">NexEstate ADMIN</strong>'
)

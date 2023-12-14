from django.contrib import admin
from apps.enquiries.models import Enquiry

# Register your models here.


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "is_answered")
    list_filter = ("is_answered",)
    search_fields = ("name", "email", "subject", "message")


admin.site.register(Enquiry, EnquiryAdmin)

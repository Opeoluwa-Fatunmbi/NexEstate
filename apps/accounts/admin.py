from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from apps.accounts.models import *
from django.utils.translation import gettext_lazy as _


# Register your models here.
class UserAdmin(BaseUserAdmin):
    list_display = ["first_name", "last_name", "is_email_verified", "created_at"]
    list_filter = list_display
    ordering = ["first_name", "last_name", "email"]

    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal Information"), {"fields": ("first_name", "last_name", "avatar")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_email_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("created_at", "updated_at", "last_login")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                ),
            },
        ),
    )

    readonly_fields = ("created_at", "updated_at")


admin.site.register(User, UserAdmin)

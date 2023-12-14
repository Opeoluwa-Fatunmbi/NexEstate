from django.contrib import admin

from .models import Property, PropertyViews, PropertyCategories


class PropertyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "price",
        "is_published",
        "is_featured",
        "is_available",
    )
    list_filter = ("is_published", "is_featured", "is_available")
    search_fields = ("title", "description", "price")


class PropertyCategoriesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
    )
    list_filter = list_display
    search_fields = ("name", "description")


# class PropertyViewsAdmin(admin.ModelAdmin):
#    list_display = (
#        "property",
#        "user",
#        "date",
#    )
#    list_filter = ("property", "user", "date")
#    search_fields = ("property", "user", "date")

admin.site.register(PropertyCategories, PropertyCategoriesAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyViews)

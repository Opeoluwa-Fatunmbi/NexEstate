from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.properties"

    def ready(self):
        import apps.properties.signals

        print("Properties app ready")

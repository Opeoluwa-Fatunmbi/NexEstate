from celery import Celery
from decouple import config
import os


SETTINGS = config("SETTINGS")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"nexestate.settings.{SETTINGS}")


app = Celery("nexestate")

app.config_from_object(
    "django.conf:settings"
)  # Load settings from a Django settings module.
app.autodiscover_tasks()

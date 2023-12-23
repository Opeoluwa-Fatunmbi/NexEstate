import os
from decouple import config

SETTINGS = config("SETTINGS")

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"nexestate.settings.{SETTINGS}")

application = get_asgi_application()

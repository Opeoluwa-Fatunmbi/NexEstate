import os
from decouple import config

SETTINGS = config("SETTINGS")

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"nexestate.settings.{SETTINGS}")

application = get_wsgi_application()

app = application

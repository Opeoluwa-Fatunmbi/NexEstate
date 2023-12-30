from .base import *
import dj_database_url

DEBUG = True

#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("POSTGRES_DB"),
#         "USER": config("POSTGRES_USER"),
#         "PASSWORD": config("POSTGRES_PASSWORD"),
#         "HOST": config("POSTGRES_HOST"),
#         "PORT": config("POSTGRES_PORT"),
#     }
# }

DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

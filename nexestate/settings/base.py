from pathlib import Path
import os
from decouple import config
import logging
import logging.config
from django.utils.log import DEFAULT_LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!


ALLOWED_HOSTS = config("ALLOWED_HOSTS").split(" ")


# Application definition

# Django apps

DJANGO_APPS = [
    "jazzmin",  # HIGH PRIORITY APP
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Third party apps

THIRD_PARTY_APPS = [
    "adrf",
    "rest_framework",
    "channels",
    "debug_toolbar",
    "django_filters",
    "cloudinary",
    "cloudinary_storage",
    "drf_spectacular",
    "phonenumber_field",
    "django_countries",
]

# Local apps

LOCAL_APPS = [
    "apps.common",
    "apps.accounts",
    "apps.properties",
    "apps.enquiries",
    "apps.payments",
    "apps.notifications",
    "apps.reports",
    "apps.analytics",
    "apps.chats",
    "apps.ratings",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "nexestate.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nexestate.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


AUTH_USER_MODEL = "accounts.User"

SITE_ID = 1

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Lagos"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static/")]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media/")


# Cloudinary settings

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# REST-FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "100/day", "user": "1000/day"},
    "DEFAULT_THROTTLE_MESSAGES": {
        "anon": "Too many requests. Please try again later.",
        "user": "Daily request limit reached. Please try again tomorrow.",
        #'custom_scope': 'You have exceeded the hourly rate limit for this view.',
    },
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


# Email Settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT")
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
EMAIL_OTP_EXPIRE_SECONDS = config("EMAIL_OTP_EXPIRE_SECONDS")


# Logging Settings
logger = logging.getLogger(__name__)

LOG_LEVEL = "INFO"

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            },
            "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "console",
            },
            "file": {
                "level": "INFO",
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": "logs/nexestate.log",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False,
            },
            "apps": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False,
            },
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }
)


SPECTACULAR_SETTINGS = {
    "TITLE": "NexEstate API",
    "DESCRIPTION": "Let us connect you with your dream home",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

INTERNAL_IPS = [
    "127.0.0.1",
]


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "NexEstate",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "NexEstate ADMIN",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "media/logo.png",
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-circle",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": "media/logo.png",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "media/logo.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to NexEstate Admin Section",
    # Copyright on the footer
    "copyright": "NexEstate Ltd",
    # The model admin to search from the search bar, search bar omitted if excluded
    "search_model": "accountsUser",
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": "avatar",
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {
            "name": "Home",
            "url": "admin:index",
            "permissions": ["auth.view_user"],
        },
        # model admin to link to (Permissions checked against model)
        # {"model": "accounts.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "accounts"},
        {"app": "analytics"},
        {"app": "enquiries"},
        {"app": "notifications"},
        {"app": "payments"},
        {"app": "properties"},
        {"app": "profiles"},
        {"app": "reports"},
        {"app": "chats"},
        {"app": "sites"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "NexEstate FrontPage", "url": "/", "new_window": True},
        {"model": "accounts.user"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    # "order_with_respect_to": ["auth", "accounts", "accounts.user", "accounts.tutor", "accounts.student", "lessons"],
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth.Group": "fas fa-users",
        "accounts.user": "fas fa-user-cog",
        "equiries.enquiry": "fas fa-envelope",
        "notifications.notification": "fas fa-bell",
        "payments.payment": "fas fa-money-bill",
        "properties.property": "fas fa-home",
        "profiles.profile": "fas fa-user",
        "reports.report": "fas fa-chart-bar",
        "chats.chat": "fas fa-comments",
        "sites.site": "fas fa-globe",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #############
    # UI Tweaks #
    #############
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # "related_modal_active": True # Won't work in some browsers
}


# Cache settings

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}


# Debug Toolbar settings

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.cache.CachePanel",
    # other panels
]


# Channels settings

ASGI_APPLICATION = "nexestate.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # Use Redis as the channel layer backend
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


# JWT Settings

ACCESS_TOKEN_LIFETIME_MINUTES = config("ACCESS_TOKEN_LIFETIME_MINUTES")
REFRESH_TOKEN_LIFETIME_MINUTES = config("REFRESH_TOKEN_LIFETIME_MINUTES")


# STRIPE SETTINGS

STRIPE_PUBLIC_KEY = config("STRIPE_PUBLIC_KEY")
SUCCESS_URL = config("SUCCESS_URL")
CANCEL_URL = config("CANCEL_URL")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")



 # GOOGLE API-KEY

GOOGLE_API_KEY = config("GOOGLE_API_KEY")
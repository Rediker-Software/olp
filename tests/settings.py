# Import all of the settings from the global settings file.
# This allows us to have our own custom settings for running tests.

from django.conf.global_settings import *
import os

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

DEBUG = True
TEMPLATE_DEBUG = True

ROOT_URLCONF = "tests.urls"

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    "olp.backends.PermissionBackend",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'olp.middleware.PatchModelsMiddleware',
)

INSTALLED_APPS = [
    "django.contrib.auth",
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    "olp",
    "tests",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "olp.db",
    }
}

OLP_SETTINGS = {
    "models": (
        ("django.contrib.auth.models.Group", "user"),
    )
}

SECRET_KEY = "notsosecretkey"
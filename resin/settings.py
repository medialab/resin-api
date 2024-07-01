"""
Django settings for resin_backend project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("RESIN_DEBUG", "True").lower() in ("true", "1")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "dummysecret" if DEBUG else os.environ.get("RESIN_SECRET")

ALLOWED_HOSTS = [os.environ.get("RESIN_HOST", "localhost")]
RESIN_DOCKER_CONTAINER = os.environ.get("RESIN_DOCKER_CONTAINER")
if RESIN_DOCKER_CONTAINER:
    ALLOWED_HOSTS.append(RESIN_DOCKER_CONTAINER)
CORS_ALLOW_ALL_ORIGINS = True


# Application definition

INSTALLED_APPS = [
    "resin.apps.ResinAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "annuaire.apps.AnnuaireConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "resin.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "resin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data/db.sqlite3",
    }
}

# Auth

AUTH_USER_MODEL = "annuaire.Member"
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
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "annuaire.auth.TokenExpirationAuthentication",
    ]
}
EDIT_PROFILE_URL = os.environ.get(
    "RESIN_EDIT_PROFILE_URL", "http://localhost:3000/profile"
)
PROFILE_URL = os.environ.get("RESIN_PROFILE_URL", "http://localhost:3000/profile")

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
MEDIA_URL = "uploads/"
MEDIA_ROOT = BASE_DIR / "uploads"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Emails
EMAIL_BACKEND = (
    "django.core.mail.backends.console.EmailBackend"
    if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = os.environ.get("RESIN_EMAIL_HOST", "localhost")
EMAIL_PORT = os.environ.get("RESIN_EMAIL_PORT", 25)
EMAIL_USE_TLS = os.environ.get("RESIN_EMAIL_TLS", "False").lower() in ("true", "1")
EMAIL_USE_SSL = os.environ.get("RESIN_EMAIL_SSL", "False").lower() in ("true", "1")
EMAIL_HOST_USER = os.environ.get("RESIN_EMAIL_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("RESIN_EMAIL_PASSWORD", "")
EMAIL_FROM = os.environ.get("RESIN_EMAIL_FROM", "admin@localhost")
EMAIL_SSL_CERTFILE = os.environ.get("RESIN_EMAIL_SSL_CERTFILE", None)
EMAIL_SSL_KEYFILE = os.environ.get("RESIN_EMAIL_SSL_KEYFILE", None)

import os
from datetime import timedelta
from pathlib import Path

import dj_database_url
import environ

# Base
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
	DEBUG=(bool, False),
)

# Read .env if present
ENV_FILE = BASE_DIR / ".env"
if ENV_FILE.exists():
	env.read_env(str(ENV_FILE))

SECRET_KEY = env("SECRET_KEY", default="change-me")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = [h for h in env("ALLOWED_HOSTS", default="*").split(",") if h]

# Applications
INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"django.contrib.staticfiles",
	# Third-party
	"rest_framework",
	"drf_spectacular",
	# Local
	"users",
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"whitenoise.middleware.WhiteNoiseMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "auth_service.urls"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
		},
	}
]

WSGI_APPLICATION = "auth_service.wsgi.application"
ASGI_APPLICATION = "auth_service.asgi.application"

# Database
DATABASES = {
	"default": dj_database_url.parse(
		env("DATABASE_URL", default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
		conn_max_age=600,
		ssl_require=False,
	)
}

# Cache (Redis for password reset tokens, etc.)
CACHES = {
	"default": {
		"BACKEND": "django_redis.cache.RedisCache",
		"LOCATION": env("REDIS_URL", default="redis://localhost:6379/1"),
		"OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
	}
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
	{"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
	{"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
	{"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
	{"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DRF / JWT / Schema
REST_FRAMEWORK = {
	"DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
	"DEFAULT_AUTHENTICATION_CLASSES": (
		"rest_framework_simplejwt.authentication.JWTAuthentication",
	),
	"DEFAULT_PERMISSION_CLASSES": (
		"rest_framework.permissions.IsAuthenticated",
	),
}

SPECTACULAR_SETTINGS = {
	"TITLE": "Auth Service API",
	"DESCRIPTION": "User authentication service with JWT and password reset",
	"VERSION": "1.0.0",
}

from rest_framework_simplejwt.settings import api_settings as jwt_settings  # noqa: E402

SIMPLE_JWT = {
	"ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
	"REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

from pathlib import Path
from datetime import timedelta
import os
from decouple import config
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG",default=False)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cloudinary_storage",
    # pip packages
    "rest_framework",
    "corsheaders",
    "django_cleanup.apps.CleanupConfig",
    # Social Auth Packages
    "oauth2_provider",
    "social_django",
    "drf_social_oauth2",
    # apps
    "auth_api",
    "Profile",
    "network",
    "post",
    "chat",
    "Job",
]

AUTH_USER_MODEL = "auth_api.User"


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


ROOT_URLCONF = "linkedin.urls"
CORS_ALLOW_ALL_ORIGINS = True
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
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

# WSGI_APPLICATION = "linkedin.wsgi.application"
ASGI_APPLICATION = "linkedin.asgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Dhaka"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
MEDIA_ROOT = MEDIA_DIR
MEDIA_URL = "/media/"


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        # django-oauth-toolkit >= 1.0.0
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
        "drf_social_oauth2.authentication.SocialAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DATETIME_FORMAT": "%m/%d/%Y %H:%M:%S",
}

from oauth2_provider import settings as oauth2_settings
from datetime import timedelta

oauth2_settings.DEFAULTS["ACCESS_TOKEN_EXPIRE_SECONDS"] = 24 * 60 * 60

AUTHENTICATION_BACKENDS = (
    # Others auth providers (e.g. Google, OpenId, etc)
    # Facebook OAuth2
    "social_core.backends.facebook.FacebookAppOAuth2",
    "social_core.backends.facebook.FacebookOAuth2",
    "social_core.backends.google.GoogleOAuth2",
    # drf_social_oauth2
    "drf_social_oauth2.backends.DjangoOAuth2",
    # Django
    "django.contrib.auth.backends.ModelBackend",
)


SOCIAL_AUTH_FACEBOOK_KEY = config("SOCIAL_AUTH_FACEBOOK_KEY")
SOCIAL_AUTH_FACEBOOK_SECRET = config("SOCIAL_AUTH_FACEBOOK_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY").split(" ")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

SOCIAL_AUTH_FACEBOOK_SCOPE = ["email"]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {"fields": "id, name, email"}
SOCIAL_AUTH_USER_FIELDS = ["email", "username", "password"]


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # "hosts": [("127.0.0.1", 6379)],
            "hosts": [("redis://:6XPs89CiLjfLzTjL4r5oLLDFTtk1PBd6@redis-19854.c44.us-east-1-2.ec2.cloud.redislabs.com:19854/0")],
        },
    },
}
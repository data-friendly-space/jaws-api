"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import logging
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

from health_checks.middlewares import IgnoreHealthCheckLogFilter
from user_management.middlewares.ignore_session_verify_logs import IgnoreSessionVerifyLogFilter

load_dotenv(override=True)
logging.getLogger("django.server").addFilter(IgnoreHealthCheckLogFilter())
logging.getLogger("django.server").addFilter(IgnoreSessionVerifyLogFilter())
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=a#w2hz%r2bw+4-6ben(5ds-2*ycf#ac$)l(jh!2^ojp++%z3g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

CSRF_TRUSTED_ORIGINS = ['http://localhost', 'https://localhost', 'http://localhost:3000']
# Application definition
CUSTOM_APPS = [
    'common',
    'user_management',
    'health_checks',
    'analysis',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'health_check',  # Required
    'health_check.cache',  # Cache backend health checker
    'health_check.storage',  # Default storage system health check
    'corsheaders',
    'social_django'
]

INSTALLED_APPS += CUSTOM_APPS

CUSTOM_MIDDLEWARES = [
    'common.middlewares.exception_handler.ExceptionHandler',
    'user_management.middlewares.jwt_middleware.JWTMiddleware',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',

]

MIDDLEWARE += CUSTOM_MIDDLEWARES
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'user_management.User'

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

SIMPLE_JWT = {
    # Duration of the access token
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', 30))),  # 30min as example

    # Duration of the refresh token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.getenv('REFRESH_TOKEN_LIFETIME', 7))),  # 7 days as example

    # Algorithm used for signing the tokens
    'ALGORITHM': 'HS256',  # Default algorithm (you can switch to RS256 for asymmetric key signing)

    # Secret key used to sign the JWT
    'SIGNING_KEY': SECRET_KEY,  # Use Django's SECRET_KEY or define a custom signing key

    # Optional: If using an asymmetric signing algorithm (e.g., RS256)
    # 'PRIVATE_KEY': open("path_to_your_private_key.pem").read(),
    # 'PUBLIC_KEY': open("path_to_your_public_key.pem").read(),

    # Additional configurations
    'AUTH_HEADER_TYPES': ('Bearer',),  # Prefix in the authentication header
    'USER_ID_FIELD': 'id',  # Field representing the user's ID
    'USER_ID_CLAIM': 'user_id',  # Claim key in the payload for the user's ID
}

WSGI_APPLICATION = 'app.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE'),
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USERNAME'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    },
}

TEST = {
    'DEPENDENCIES': 'keepdb',
}

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Social auth
SOCIAL_AUTH_USER_MODEL = 'user_management.User'
SOCIAL_AUTH_JSONFIELD_ENABLED = True
USERNAME_IS_FULL_EMAIL = True

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv("GOOGLE_AUTH_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv("GOOGLE_AUTH_SECRET")

SOCIAL_AUTH_LOGIN_REDIRECT_URL = "http://localhost:3000/workspaces"

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    # Disabled by default
    # 'social_core.pipeline.mail.mail_validation',
    # Disabled by default
    # 'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'user_management.social_auth.pipeline.redirect_to_next_with_token'
)

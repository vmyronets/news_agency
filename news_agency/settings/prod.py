from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["127.0.0.1", ]

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': os.getenv("POSTGRES_DB"),
        'USER': os.getenv("POSTGRES_USER"),
        'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
        'HOST': os.getenv("POSTGRES_HOST"),
        'PORT': int(os.getenv("POSTGRES_DB_PORT")),
        'OPTIONS': {
            'sslmode': 'require'
        }
    }
}

SESSION_COOKIE_SECURE = True

SECURE_SSL_REDIRECT = True

CSRF_COOKIE_SECURE = True

from .base import *
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
  }
}

# DATABASES = {
#   'default': {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': os.getenv('POSTGRES_DB'),
#     'USER': os.getenv('POSTGRES_USER'),
#     'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#     'HOST': os.getenv('POSTGRES_HOST'),
#     'PORT': os.getenv('POSTGRES_PORT', '5432'),
#   }
# }

SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
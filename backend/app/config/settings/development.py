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
#     'NAME': os.getenv('POSTGRES_DB', 'dev_db'),
#     'USER': os.getenv('POSTGRES_USER', 'postgres'),
#     'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
#     'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
#     'PORT': '5432',
#   }
# }
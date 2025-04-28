import os
from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
API_VERSION = "1.0.1" # Version de la API
ALLOWED_HOSTS = [config('ALLOWED_HOSTS')]

INSTALLED_APPS = [
  # Django default apps
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',

  # Dependencies
  'rest_framework',
  'rest_framework_simplejwt.token_blacklist',
  'drf_spectacular',
  'django_filters',

  # Apps locales
  'core',
  'accounts',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',

  # Middleware para permitir peticiones de backend a frontend
  "corsheaders.middleware.CorsMiddleware",
  
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',

  # 👇 Middleware que dependan de la authentication van despues de este
  'django.contrib.auth.middleware.AuthenticationMiddleware',

  # Middleware para actualizar la actividad del usuario
  'core.middleware.update_user_info.UpdateUserInfoMiddleware',
  # Middleware para obtener el idioma del usuario
  'core.middleware.language_from_user.LanguageFromUserMiddleware',
  # Middleware para guardar el usuario del request
  'core.middleware.thread_user.ThreadLocalUserMiddleware',

  'django.middleware.locale.LocaleMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {}

AUTH_PASSWORD_VALIDATORS = [
  {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
  {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
  {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
  {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
  ('es', 'Español'),
  ('en', 'English'),
]

LOCALE_PATHS = [
  os.path.join(BASE_DIR, 'locale'),
]

# Permisos definidos por defecto
PROJECT_PERMISSION_APPS = [
  'auth',
  'accounts',
  'core',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Toma por default el usuario del modelo accounts
AUTH_USER_MODEL = 'accounts.User'

# Documentation settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
SPECTACULAR_SETTINGS = {
  'TITLE': 'Sistema de Autenticación y Auditoría',
  'DESCRIPTION': 'Este sistema fue diseñado como una base sólida para aplicaciones empresariales, médicas, financieras o de alta auditoría.',
  'VERSION': API_VERSION,
}

# Configuracion de Rest Framework
REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
  'DEFAULT_AUTHENTICATION_CLASSES': ('core.authentication.CustomJWTAuthentication', ),
  'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated', ),
  'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 10,
  'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
  'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S %Z',
}

# Configuracion JWT
SIMPLE_JWT = {
  'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
  'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
  'ROTATE_REFRESH_TOKENS': False,
  'BLACKLIST_AFTER_ROTATION': True,
  
  'AUTH_HEADER_TYPES': ('Bearer',),
  'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

  'TOKEN_BLACKLIST_ENABLED': True,
}

# Cors Headers authorization
# Se le coloca las urls del localhost que podra hacer peticiones
CORS_ALLOWED_ORIGINS = []
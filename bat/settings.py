"""
Django settings for bat project.
Безопасность: SECRET_KEY и DEBUG — только из переменных окружения в продакшене.
"""
import os
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Критично: SECRET_KEY только из env в продакшене. Локально — fallback.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-dev-only-change-in-production'
)

# DEBUG: по умолчанию False. Только явно DJANGO_DEBUG=1 для локальной разработки.
DEBUG = os.environ.get('DJANGO_DEBUG', '0') == '1'

_allowed = [
    h.strip() for h in
    os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost,testserver').split(',')
    if h.strip()
]
if DEBUG:
    _allowed.extend(['testserver', 'localhost'])
# Render: добавляем хост сервиса
if render_host := os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
    _allowed.append(render_host)
ALLOWED_HOSTS = list(dict.fromkeys(_allowed))  # без дубликатов

INSTALLED_APPS = [
    'bat.apps.BatConfig',  # runserver с HTTPS по умолчанию
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'batteries',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bat.urls'

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

WSGI_APPLICATION = 'bat.wsgi.application'

# База: PostgreSQL на Render (DATABASE_URL) или SQLite локально
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    _db_path = os.environ.get('DJANGO_DB_PATH') or (BASE_DIR / 'db.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(_db_path),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = 'batteries:my_submissions'
LOGOUT_REDIRECT_URL = 'batteries:home'

# ——— Безопасность для продакшена (когда DEBUG=False) ———
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', '1') == '1'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    # За прокси (Nginx, Cloudflare и т.д.):
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # Доверенные источники для CSRF (домен сайта):
    _origins = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in _origins.split(',') if o.strip()]
    # Render: автоматически добавляем HTTPS-домен
    if render_host := os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
        CSRF_TRUSTED_ORIGINS = list(dict.fromkeys(CSRF_TRUSTED_ORIGINS + [f'https://{render_host}']))

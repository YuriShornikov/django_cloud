from pathlib import Path
from pathlib import Path
from decouple import config
import os
import environ

import socket
import requests

# Определение BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# Загрузка переменных окружения
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Функция для проверки локального окружения
def is_local():
    """Определяет, работает ли сервер в локальной сети."""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)

        # Если IP в диапазоне 127.0.0.1 или 192.168.*, считаем сервер локальным
        if local_ip.startswith(("127.", "192.168.")):
            return True

        # Проверка на переменную среды IS_SERVER, указывающую, что сервер продакшен
        if os.getenv("IS_SERVER") == "true":
            return False

        # Проверяем, есть ли локальный IP в сети
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Подключаемся к Google DNS
        test_socket.connect(("8.8.8.8", 80))
        network_ip = test_socket.getsockname()[0]
        test_socket.close()

        if network_ip.startswith(("192.168.", "10.", "172.")):
            # Сервер находится в локальной сети
            return True

    except (socket.gaierror, socket.error):
        # В случае ошибки считаем сервер локальным
        return True

    # Если не сработал ни один вариант, считаем, что это продакшен
    return False

# Функция для получения внешнего IP сервера
def get_external_ip():
    """Получает внешний IP сервера."""
    try:
        response = requests.get("https://api64.ipify.org?format=text", timeout=3)
        return response.text.strip()
    except requests.RequestException:
        return None

# Автоматическое определение BASE_URL
def get_base_url():
    """Определяет BASE_URL автоматически."""
    if is_local():
        return "http://localhost:8000"

    external_ip = get_external_ip()
    if external_ip:
        return f"http://{external_ip}:8000"

    return "http://localhost:8000"

BASE_URL = get_base_url()

# Настройка ALLOWED_HOSTS
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "localhost:5173",
]

if not is_local():
    external_ip = get_external_ip()
    if external_ip:
        ALLOWED_HOSTS.append(external_ip)

# Пути для сохранения загруженных файлов
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = True


SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600
# SESSION_SAVE_EVERY_REQUEST = True

# Настройки CSRF
# CSRF_TRUSTED_ORIGINS = ["http://localhost:5173"]
CSRF_TRUSTED_ORIGINS = [f"http://{host}" for host in ALLOWED_HOSTS]
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False  # Должен быть True для (HTTPS)
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
CSRF_USE_SESSIONS = False

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'localhost:5173', '', '79.174.92.124', '79.174.80.81']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'users',
    'storage',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django.contrib.sites',
    # 'users.apps.UsersConfig',
]

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mycloud.urls'

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

WSGI_APPLICATION = 'mycloud.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Статические файлы
STATIC_ROOT=os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser'

APPEND_SLASH = False

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

CORS_ALLOW_HEADERS = [
    'content-type',
    'authorization',
    'accept',
    'origin',
    'x-csrftoken',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Включаем поддержку временных зон
USE_TZ = True

# Устанавливаем нужную временную зону
TIME_ZONE = 'Europe/Moscow'

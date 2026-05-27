# ============================================================
# ФАЙЛ: django_project/settings.py
# НАЗНАЧЕНИЕ: Центральный конфигурационный файл Django-проекта.
#   Содержит все параметры приложения: безопасность, базы данных,
#   подключённые приложения, пути к файлам, локализацию.
# ============================================================

# ---------------------------------------------------------------
# БЛОК ИМПОРТОВ СТАНДАРТНЫХ МОДУЛЕЙ
# ---------------------------------------------------------------
import os           # Чтение переменных окружения (доменные имена Replit)
from pathlib import Path  # Современный способ работы с путями файловой системы

# ---------------------------------------------------------------
# БЛОК БАЗОВЫХ ПУТЕЙ ПРОЕКТА
# BASE_DIR — корневая директория проекта (там, где лежит manage.py)
# ---------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # Два уровня вверх от settings.py

# ---------------------------------------------------------------
# БЛОК БЕЗОПАСНОСТИ
# ---------------------------------------------------------------
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4ju2n@$f9d0c=h)_g0lbb%k9&@rf(xa$d$g$&5ri$uf)*gev^4')

DEBUG = True
# ^ Режим отладки: True — подробные ошибки в браузере.
#   В production ОБЯЗАТЕЛЬНО установить False.

# Список разрешённых хостов: берём из переменной окружения Replit, добавляем localhost
ALLOWED_HOSTS = os.environ.get("REPLIT_DOMAINS", "localhost").split(',') + ['localhost', '0.0.0.0']

# Доверенные источники для CSRF-защиты (Replit проксирует через HTTPS)
_replit_domains = [d for d in os.environ.get("REPLIT_DOMAINS", "").split(',') if d]
CSRF_TRUSTED_ORIGINS = []
for _domain in _replit_domains:
    CSRF_TRUSTED_ORIGINS.append(f"https://{_domain}")
    CSRF_TRUSTED_ORIGINS.append(f"https://{_domain}:80")
    CSRF_TRUSTED_ORIGINS.append(f"https://{_domain}:443")
    CSRF_TRUSTED_ORIGINS.append(f"https://{_domain}:8000")
    CSRF_TRUSTED_ORIGINS.append(f"https://{_domain}:3000")
    CSRF_TRUSTED_ORIGINS.append(f"https://{_domain}:5000")

# ---------------------------------------------------------------
# БЛОК ПОДКЛЮЧЁННЫХ ПРИЛОЖЕНИЙ
# Перечень всех активных модулей Django и сторонних библиотек
# ---------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',          # Встроенная административная панель Django
    'django.contrib.auth',           # Система аутентификации пользователей
    'django.contrib.contenttypes',   # Типы контента (нужен для auth и admin)
    'django.contrib.sessions',       # Хранение пользовательских сессий
    'django.contrib.messages',       # Одноразовые сообщения (flash messages)
    'django.contrib.staticfiles',    # Обслуживание статических файлов (CSS, JS)
    'tasks',                         # Основное приложение микросервиса
]

# ---------------------------------------------------------------
# БЛОК ПРОМЕЖУТОЧНОГО ПРОГРАММНОГО ОБЕСПЕЧЕНИЯ (MIDDLEWARE)
# Слои обработки каждого входящего запроса (выполняются по порядку)
# ---------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',          # Заголовки безопасности (HTTPS, HSTS)
    'django.contrib.sessions.middleware.SessionMiddleware',   # Поддержка сессий пользователей
    'django.middleware.common.CommonMiddleware',              # Нормализация URL (слеш в конце)
    'django.middleware.csrf.CsrfViewMiddleware',              # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',# Привязка пользователя к запросу
    'django.contrib.messages.middleware.MessageMiddleware',   # Передача flash-сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от clickjacking (X-Frame-Options)
]

# В production добавляем дополнительный clickjacking-middleware
if "REPLIT_DEPLOYMENT" in os.environ:
    MIDDLEWARE.append('django.middleware.clickjacking.XFrameOptionsMiddleware')

# ---------------------------------------------------------------
# БЛОК МАРШРУТИЗАЦИИ URL
# ---------------------------------------------------------------
ROOT_URLCONF = 'django_project.urls'  # Главный файл URL-маршрутов проекта

# ---------------------------------------------------------------
# БЛОК ШАБЛОНОВ HTML
# Настройки движка шаблонов Django (Jinja-подобный синтаксис)
# ---------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],       # Дополнительные директории с шаблонами (не используются)
        'APP_DIRS': True, # Искать шаблоны в папках templates/ внутри каждого приложения
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',    # Переменная debug в шаблонах
                'django.template.context_processors.request',  # Объект request в шаблонах
                'django.contrib.auth.context_processors.auth', # Данные пользователя в шаблонах
                'django.contrib.messages.context_processors.messages',  # Flash-сообщения
            ],
        },
    },
]

# ---------------------------------------------------------------
# БЛОК WSGI/ASGI КОНФИГУРАЦИИ
# Точки входа для веб-серверов
# ---------------------------------------------------------------
WSGI_APPLICATION = 'django_project.wsgi.application'  # Для синхронных серверов (gunicorn, uWSGI)

# ---------------------------------------------------------------
# БЛОК БАЗЫ ДАННЫХ
# Проект использует SQLite — встроенную базу данных, хранящуюся в одном файле
# ---------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Движок SQLite (не требует отдельного сервера)
        'NAME': BASE_DIR / 'db.sqlite3',         # Путь к файлу базы данных
    }
}

# ---------------------------------------------------------------
# БЛОК ВАЛИДАЦИИ ПАРОЛЕЙ
# Набор правил проверки сложности паролей пользователей
# ---------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    # ^ Запрещает пароли, похожие на имя пользователя или email
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    # ^ Минимальная длина пароля (по умолчанию 8 символов)
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    # ^ Запрещает распространённые пароли (123456, password и т.п.)
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    # ^ Запрещает пароли, состоящие только из цифр
]

# ---------------------------------------------------------------
# БЛОК ИНТЕРНАЦИОНАЛИЗАЦИИ
# ---------------------------------------------------------------
LANGUAGE_CODE = 'en-us'   # Язык интерфейса Django Admin и системных сообщений
TIME_ZONE = 'UTC'         # Часовой пояс для хранения дат в базе данных
USE_I18N = True           # Включить поддержку переводов интерфейса
USE_TZ = True             # Использовать timezone-aware datetime объекты

# ---------------------------------------------------------------
# БЛОК СТАТИЧЕСКИХ И МЕДИА-ФАЙЛОВ
# ---------------------------------------------------------------
STATIC_URL = 'static/'   # URL-префикс для статических файлов (CSS, JS, иконки)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# ^ Тип поля первичного ключа по умолчанию (64-битный целочисленный ID)

MEDIA_URL = '/media/'                              # URL-префикс для медиафайлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')      # Физическая директория хранения медиафайлов

# ---------------------------------------------------------------
# БЛОК АУТЕНТИФИКАЦИИ
# ---------------------------------------------------------------
LOGIN_URL = '/login/'          # Адрес страницы входа (переопределяем стандартный /accounts/login/)
LOGIN_REDIRECT_URL = '/'       # После успешного входа перенаправляем на главную страницу
LOGOUT_REDIRECT_URL = '/login/'  # После выхода — на страницу входа

# Cookie-настройки для работы в iframe (Replit preview)
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

# Настройки CSRF для работы в Replit
CSRF_TRUSTED_ORIGINS = [
    'https://*.replit.dev',
    'https://*.replit.co',
    'http://*.replit.dev',
    'http://*.replit.co',
]
CSRF_COOKIE_SECURE = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False

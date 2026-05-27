import os  # Импорт модуля для работы с переменными окружения
from pathlib import Path  # Импорт класса Path для кроссплатформенной работы с путями

BASE_DIR = Path(__file__).resolve().parent.parent  # Определение корневой директории проекта (два уровня вверх)

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-4ju2n@$f9d0c=h)_g0lbb%k9&@rf(xa$d$g$&5ri$uf)*gev^4')  # Секретный ключ Django (берётся из окружения или используется запасной)

DEBUG = True  # Режим отладки включён (показывает детальные ошибки в браузере)

ALLOWED_HOSTS = ['*']  # Разрешены все хосты (для работы в любой среде, включая Replit)

INSTALLED_APPS = [  # Список установленных приложений Django
    'django.contrib.admin',  # Административная панель
    'django.contrib.auth',  # Система аутентификации
    'django.contrib.contenttypes',  # Типы контента (нужен для auth)
    'django.contrib.sessions',  # Управление сессиями пользователей
    'django.contrib.messages',  # Система flash-сообщений
    'django.contrib.staticfiles',  # Обслуживание статических файлов
    'tasks',  # Основное приложение микросервиса
]

MIDDLEWARE = [  # Список промежуточных обработчиков запросов
    'django.middleware.security.SecurityMiddleware',  # Заголовки безопасности
    'django.contrib.sessions.middleware.SessionMiddleware',  # Поддержка сессий
    'django.middleware.common.CommonMiddleware',  # Нормализация URL (добавление слеша)
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Привязка пользователя к запросу
    'django.contrib.messages.middleware.MessageMiddleware',  # Передача flash-сообщений
]

# Allow site to be displayed inside Replit preview iframe  # Разрешает отображение сайта во фрейме Preview Replit
X_FRAME_OPTIONS = 'ALLOWALL'  # Отключает защиту от clickjacking (нужно для Preview)

ROOT_URLCONF = 'django_project.urls'  # Указывает главный файл маршрутизации URL

TEMPLATES = [  # Настройки шаблонизатора Django
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Используется стандартный движок Django
        'DIRS': [],  # Дополнительные директории с шаблонами (пусто)
        'APP_DIRS': True,  # Разрешает поиск шаблонов в папке templates каждого приложения
        'OPTIONS': {
            'context_processors': [  # Процессоры контекста (передают переменные в шаблоны)
                'django.template.context_processors.debug',  # Переменная debug в шаблонах
                'django.template.context_processors.request',  # Объект request в шаблонах
                'django.contrib.auth.context_processors.auth',  # Данные пользователя в шаблонах
                'django.contrib.messages.context_processors.messages',  # Flash-сообщения
            ],
        },
    },
]

WSGI_APPLICATION = 'django_project.wsgi.application'  # Точка входа для WSGI-серверов

DATABASES = {  # Настройки базы данных
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Используется SQLite (встроенная БД)
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
    }
}

AUTH_PASSWORD_VALIDATORS = [  # Валидаторы сложности паролей
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},  # Запрещает пароли, похожие на имя пользователя
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},  # Проверяет минимальную длину пароля
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},  # Запрещает распространённые пароли
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},  # Запрещает пароли из цифр
]

LANGUAGE_CODE = 'en-us'  # Язык интерфейса (английский)
TIME_ZONE = 'UTC'  # Часовой пояс (UTC)
USE_I18N = True  # Включает поддержку интернационализации
USE_TZ = True  # Включает поддержку timezone-aware дат

STATIC_URL = 'static/'  # URL-префикс для статических файлов
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Тип поля первичного ключа по умолчанию (64-битный ID)
MEDIA_URL = '/media/'  # URL-префикс для медиафайлов
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Физическая директория для хранения медиафайлов

LOGIN_URL = '/login/'  # Адрес страницы входа (переопределяем стандартный)
LOGIN_REDIRECT_URL = '/'  # После успешного входа перенаправляем на главную страницу
LOGOUT_REDIRECT_URL = '/login/'  # После выхода перенаправляем на страницу входа

# Cookie settings for iframe (Replit preview)  # Настройки cookie для работы в iframe Preview
SESSION_COOKIE_SAMESITE = 'Lax'  # Политика SameSite для cookie сессии ('Lax' разрешает передачу внутри iframe)
SESSION_COOKIE_SECURE = False  # Отключает требование HTTPS для cookie (для http в Replit)
SESSION_COOKIE_HTTPONLY = False  # Разрешает доступ к cookie через JavaScript (нужно для работы внутри iframe)
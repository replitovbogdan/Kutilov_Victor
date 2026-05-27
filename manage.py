#!/usr/bin/env python
# ============================================================
# ФАЙЛ: manage.py
# НАЗНАЧЕНИЕ: Точка входа командной строки Django.
#   Используется для запуска сервера, миграций, создания
#   суперпользователя и других административных задач.
#
# Примеры использования:
#   python manage.py runserver 0.0.0.0:5000  — запуск сервера
#   python manage.py migrate                  — применение миграций БД
#   python manage.py createsuperuser         — создание администратора
# ============================================================

import os   # Установка переменной окружения с путём к настройкам
import sys  # Получение аргументов командной строки


def main():
    """Точка входа: читает команду из аргументов и передаёт её Django."""

    # Указываем Django, где находится файл настроек проекта
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

    try:
        from django.core.management import execute_from_command_line
        # ^ Импортируем Django только здесь — если его нет, выдаём понятную ошибку
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    execute_from_command_line(sys.argv)
    # ^ Выполняет команду из командной строки (например, "runserver 0.0.0.0:5000")


if __name__ == '__main__':
    main()  # Запускается только при прямом вызове: python manage.py <команда>

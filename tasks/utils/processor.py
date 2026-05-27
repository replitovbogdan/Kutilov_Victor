# ============================================================
# ФАЙЛ: tasks/utils/processor.py
# НАЗНАЧЕНИЕ: Ядро микросервиса — обработка файлов, генерация
#             статистики и построение графиков
# ============================================================

import pandas as pd        # Библиотека для чтения CSV-файлов
import json                # Встроенный модуль для чтения JSON-файлов
import os                  # Работа с файловой системой
from datetime import datetime  # Замер времени обработки
import matplotlib
matplotlib.use('Agg')      # Нет дисплея на сервере — используем не-интерактивный бэкенд
import matplotlib.pyplot as plt  # Построение графиков
import numpy as np         # Математические операции (генерация тестовых данных)
from django.conf import settings  # Доступ к настройкам Django-проекта

# ---------------------------------------------------------------
# БЛОК НАСТРОЙКИ ГРАФИКОВ
# Задаём шрифт и параметры отображения для всех графиков проекта
# ---------------------------------------------------------------
plt.rcParams['font.family'] = ['DejaVu Sans']  # Шрифт, поддерживающий кириллицу
plt.rcParams['axes.unicode_minus'] = False     # Корректное отображение знака минус


# ===============================================================
# БЛОК ХРАНЕНИЯ И ЗАГРУЗКИ ДАННЫХ
# Класс DataStorage — контейнер безопасности для загрузки файлов.
# Читает файл, определяет его формат, измеряет время загрузки
# и фиксирует результат (success / failed).
# ===============================================================

class DataStorage:
    def __init__(self):
        self.processed_files = []  # Список результатов обработки всех файлов

    def load_file(self, filename):
        """Загружает один файл, определяет формат, измеряет время."""

        # Шаблон записи результата для одного файла
        file_info = {
            "filename": filename,
            "format": "unknown",   # Формат определяется ниже
            "load_time": 0,        # Время загрузки в секундах
            "error": "",           # Текст ошибки (если есть)
            "status": ""           # "success" или "failed"
        }

        start_time = datetime.now()  # Фиксируем момент начала загрузки

        try:
            if not os.path.exists(filename):
                raise FileNotFoundError("File not found")  # Файл не найден

            if filename.endswith('.json'):
                # --- Обработка JSON-файла ---
                f = open(filename, 'r')
                data = json.load(f)   # Парсинг JSON в словарь Python
                f.close()
                file_info["format"] = "JSON"
                file_info["status"] = "success"

            elif filename.endswith('.csv'):
                # --- Обработка CSV-файла ---
                data = pd.read_csv(filename)  # Чтение CSV через Pandas
                file_info["format"] = "CSV"
                file_info["status"] = "success"

            else:
                # --- Неизвестный формат — угроза безопасности ---
                raise ValueError("Unknown format")  # Формат не поддерживается

        except Exception as e:
            # Любая ошибка → статус "failed", данные замещаются резервными
            file_info["status"] = "failed"
            file_info["error"] = str(e)           # Сохраняем текст ошибки
            data = {"file": filename, "status": "reserve data"}  # Резервные данные

        end_time = datetime.now()
        # Вычисляем время загрузки в секундах с миллисекундной точностью
        file_info["load_time"] = (end_time - start_time).total_seconds()

        self.processed_files.append(file_info)  # Добавляем результат в журнал
        return data

    def get_results(self):
        """Возвращает весь список результатов обработки файлов."""
        return self.processed_files


# ===============================================================
# БЛОК СОЗДАНИЯ ТЕСТОВЫХ ФАЙЛОВ
# Генерирует 5 тестовых файлов (3 JSON + 2 CSV) для демонстрации
# работы микросервиса при первом запуске приложения.
# ===============================================================

def create_test_files():
    """Создание тестовых файлов для демонстрации работы."""
    print("СОЗДАНИЕ ТЕСТОВЫХ ФАЙЛОВ")

    # Тестовый JSON-файл №1 — простой набор данных
    json_data1 = {"name": "Test Data", "values": [6, 2, 3, 4, 5]}
    f = open('data.json', 'w')
    json.dump(json_data1, f)   # Сериализуем словарь в JSON и записываем в файл
    f.close()
    print("  Создан: data.json")

    # Тестовый JSON-файл №2 — список отчётов
    json_data2 = {"reports": ["report1", "report2", "report3"]}
    f = open('report.json', 'w')
    json.dump(json_data2, f)
    f.close()
    print("  Создан: report.json")

    # Тестовый JSON-файл №3 — конфигурационные параметры
    json_data3 = {"config": {"debug": True, "timeout": 30}}
    f = open('config.json', 'w')
    json.dump(json_data3, f)
    f.close()
    print("  Создан: config.json")

    # Тестовый CSV-файл №1 — таблица пользователей
    csv_data1 = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]
    })
    csv_data1.to_csv('data.csv', index=False)  # Сохраняем DataFrame в CSV без индекса
    print("  Создан: data.csv")

    # Тестовый CSV-файл №2 — временной ряд со случайными значениями
    csv_data2 = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=5),  # 5 дат подряд
        'Value': np.random.randn(5)                       # 5 случайных чисел
    })
    csv_data2.to_csv('backup.csv', index=False)
    print("  Создан: backup.csv")

    print("\nВсе тестовые файлы успешно созданы!")


# ===============================================================
# БЛОК ПАКЕТНОЙ ОБРАБОТКИ ФАЙЛОВ
# Принимает список путей к файлам, последовательно загружает
# каждый через DataStorage и возвращает сводный список результатов.
# ===============================================================

def process_files(file_list):
    """Обработка списка файлов — основная точка входа для обработки."""
    storage = DataStorage()  # Создаём новый контейнер для текущего сеанса

    print("\nФайлы для обработки:")
    for f in file_list:
        print("  - " + f)

    for file in file_list:
        storage.load_file(file)  # Загружаем каждый файл и сохраняем результат

    return storage.get_results()  # Возвращаем список словарей с результатами


# ===============================================================
# БЛОК ВИЗУАЛИЗАЦИИ РЕЗУЛЬТАТОВ
# Генерирует 4 графика по итогам обработки файлов и сохраняет
# их как PNG-файлы на диск для последующей отдачи в браузер.
# ===============================================================

def generate_charts(results):
    """Генерация 4 графиков на основе результатов обработки файлов."""

    # --- Подсчёт статистики по статусам ---
    success_count = sum(1 for r in results if r['status'] == 'success')  # Кол-во успешных
    failed_count = sum(1 for r in results if r['status'] != 'success')   # Кол-во ошибочных

    # ---------------------------------------------------------------
    # График 1 (char7.png): Круговая диаграмма — распределение статусов
    # ---------------------------------------------------------------
    fig, ax = plt.subplots()
    ax.pie(
        [success_count, failed_count],
        labels=None,
        autopct=None,
        shadow=True,
        wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"}  # Пунктирная граница
    )
    ax.axis("equal")  # Круг (не эллипс)
    plt.title('Распределение статусов загрузки файлов', fontsize=12, fontweight='bold')
    plt.savefig('char7.png', dpi=100, bbox_inches='tight')  # Сохранение в PNG
    plt.close()

    # ---------------------------------------------------------------
    # График 2 (char8.png): Столбчатая диаграмма — время загрузки по файлам
    # ---------------------------------------------------------------
    filenames = [r['filename'] for r in results]    # Названия файлов
    load_times = [r['load_time'] for r in results]  # Времена загрузки
    colors = ['green' if r['status'] == 'success' else 'red' for r in results]  # Цвет по статусу

    plt.figure(figsize=(12, 6))
    plt.bar(filenames, load_times, color=colors, edgecolor='black')
    plt.xlabel('Название файла', fontsize=12)
    plt.ylabel('Время загрузки (секунды)', fontsize=12)
    plt.title('Время загрузки по файлам', fontsize=14, fontweight='bold')
    plt.xticks(rotation=45, ha='right')  # Подписи по оси X — под углом 45°
    plt.tight_layout()
    plt.savefig('char8.png', dpi=100, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------------
    # График 3 (char9.png): Круговая диаграмма — успешные vs ошибочные
    # ---------------------------------------------------------------
    fig, ax = plt.subplots()
    ax.pie(
        [success_count, failed_count],
        labels=None, autopct=None, shadow=True,
        wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"}
    )
    ax.axis("equal")
    plt.title('Сравнение успешных и неудачных загрузок', fontsize=12, fontweight='bold')
    plt.savefig('char9.png', dpi=100, bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------------
    # График 4 (char10.png): Среднее время загрузки по форматам файлов
    # ---------------------------------------------------------------
    json_times = [r['load_time'] for r in results if r['status'] == 'success' and r['format'] == 'JSON']
    csv_times  = [r['load_time'] for r in results if r['status'] == 'success' and r['format'] == 'CSV']

    formats = []
    avg_times = []

    if json_times:
        formats.append('JSON')
        avg_times.append(sum(json_times) / len(json_times))  # Среднее по JSON-файлам

    if csv_times:
        formats.append('CSV')
        avg_times.append(sum(csv_times) / len(csv_times))    # Среднее по CSV-файлам

    if formats:
        plt.figure(figsize=(8, 6))
        plt.bar(formats, avg_times, color='skyblue', edgecolor='black')
        plt.xlabel('Формат файла', fontsize=12)
        plt.ylabel('Среднее время загрузки (секунды)', fontsize=12)
        plt.title('Среднее время загрузки по форматам файлов', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('char10.png', dpi=100, bbox_inches='tight')
        plt.close()

    print("Графики сохранены: char7.png, char8.png, char9.png, char10.png")


# ===============================================================
# БЛОК ОТЛАДОЧНОГО ВЫВОДА
# Выводит результаты обработки в консоль в табличном виде.
# Используется для отладки при разработке, не вызывается из UI.
# ===============================================================

def show_results(results):
    """Вывод результатов в консоль (для отладки)."""
    print("ТАБЛИЧНОЕ ПРЕДСТАВЛЕНИЕ")
    print(f"{'Название файла':<20} {'Время (сек)':<20} {'Статус':<10} {'Ошибка':<30}")
    for result in results:
        filename  = result['filename']
        load_time = f"{result['load_time']:.3f}"
        status    = result['status'].upper()
        error     = result['error'] if result['error'] else "-"
        print(f"{filename:<20} {load_time:<20} {status:<10} {error:<30}")

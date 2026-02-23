# Macroeconomic Data Analysis Tool

CLI-утилита для обработки CSV-файлов с макроэкономическими данными и формирования аналитических отчетов.

## 🛠 Стек технологий
- **Python 3.12** (Standard Library: `argparse`, `csv`, `collections`)
- **Tabulate** (Визуализация таблиц в консоли)
- **Pytest** & **Pytest-cov** (Тестирование и контроль покрытия)

## 🚀 Запуск и использование
Скрипт поддерживает объединение данных из нескольких файлов в один отчет.

```bash
# Установка зависимости для вывода таблиц
pip -r requirements.txt

# Запуск формирования отчета по среднему ВВП
python3 macro_reports.py --files economic1.csv economic2.csv --report average-gdp
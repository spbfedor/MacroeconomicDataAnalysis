import argparse
import csv
import sys
from collections import defaultdict
from tabulate import tabulate

REPORT_REGISTRY = {}

def register_report(name):
    def decorator(func):
        REPORT_REGISTRY[name] = func
        return func
    return decorator

@register_report("average-gdp")
def average_gdp(filenames):
    data = defaultdict(list)
    for file in filenames:
        try:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        country = row['country']
                        gdp = float(row['gdp'])
                        data[country].append(gdp)
                    except (ValueError, KeyError): 
                        continue
        except FileNotFoundError:
            sys.stderr.write(f"GПредупреждение: файл {file} не найден")
    report_data = []
    for country, gdp_list in data.items():
        avg_gdp = sum(gdp_list) / len(gdp_list)
        report_data.append([country, round(avg_gdp, 2)])

    return sorted(report_data, key=lambda x: x[1], reverse=True)

def main():
    parser = argparse.ArgumentParser(description="Обработка CSV-файлов")
    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help="Пути к CSV-файлам"
    )
    parser.add_argument(
        '--report',
        choices=REPORT_REGISTRY.keys(),
        required=True,
        help="Тип отчета"
    )
    args = parser.parse_args()

    report_func = REPORT_REGISTRY[args.report]
    results = report_func(args.files)

    if results:
        sorted_result = sorted(results, key=lambda x: x[1], reverse=True)
        print(
            tabulate(
                sorted_result,
                headers=["Country", "Average GDP"],
                tablefmt="grid"
            )
        )
    else:
        sys.stderr.write("Нет данных для отчета.\n")

if __name__ == "__main__":
    main()
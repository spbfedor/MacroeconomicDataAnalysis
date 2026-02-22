import argparse
import csv
# from tabulate import tabulate

REPORT_REGISTRY = {}

def register_report(name):
    def decorator(func):
        REPORT_REGISTRY[name] = func
        return func
    return decorator

@register_report("average-gdp")
def average_gdp(filenames):
    pass

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

    print(results)

if __name__ == "__main__":
    main()
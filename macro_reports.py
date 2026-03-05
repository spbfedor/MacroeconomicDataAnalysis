import argparse
import sys
from typing import List

from tabulate import tabulate

import app.reports
from app.base import REPORT_REGISTRY
from app.schemas import CountryData


def main() -> None:
    parser = argparse.ArgumentParser(description="Обработка CSV-файлов")
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV-файлам"
    )
    parser.add_argument(
        "--report",
        choices=REPORT_REGISTRY.keys(),
        required=True,
        help="Тип отчета"
    )
    args = parser.parse_args()

    report_class = REPORT_REGISTRY[args.report]
    report_instance = report_class()
    results: List[CountryData] = report_instance.calculate(args.files)

    if results:
        table_data = [[r.country, r.gdp] for r in results]
        print(
            tabulate(
                table_data,
                headers=["Country", "Average GDP"],
                tablefmt="grid"
            )
        )
    else:
        sys.stderr.write("Нет данных для отчета.\n")


if __name__ == "__main__":
    main()

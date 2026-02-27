import argparse
import csv
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Dict, Final, List

from tabulate import tabulate

DEFAULT_ENCODING: Final[str] = "utf-8"
REPORT_FILENAME: Final[str] = "report.txt"
REPORT_REGISTRY: Dict[str, Callable] = {}


@dataclass(frozen=True)
class CountryData:
    country: str
    gdp: float


def register_report(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        REPORT_REGISTRY[name] = func
        return func

    return decorator


@register_report("average-gdp")
def average_gdp(filenames: List[str]) -> List[CountryData]:
    data: Dict[str, List[float]] = defaultdict(list)
    for file in filenames:
        try:
            with open(file, "r", encoding=DEFAULT_ENCODING) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        country = row["country"].strip()
                        gdp = float(row["gdp"])
                        data[country].append(gdp)
                    except (ValueError, KeyError):
                        continue
        except FileNotFoundError:
            sys.stderr.write(f"Предупреждение: файл {file} не найден")
    report_data: List[CountryData] = []
    for country, gdp_list in data.items():
        avg_gdp = sum(gdp_list) / len(gdp_list)
        row = CountryData(country=country, gdp=round(avg_gdp, 2))
        report_data.append(row)

    return sorted(report_data, key=lambda x: x.gdp, reverse=True)


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

    report_func = REPORT_REGISTRY[args.report]
    results: List[CountryData] = report_func(args.files)

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

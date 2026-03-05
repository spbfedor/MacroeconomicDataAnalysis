import csv
import sys
from collections import defaultdict
from typing import Dict, List

from app.base import BaseReport, register_report
from app.core import DEFAULT_ENCODING
from app.schemas import CountryData


@register_report("average-gdp")
class AverageGDPReport(BaseReport):
    def calculate(self, filenames: List[str]) -> List[CountryData]:
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

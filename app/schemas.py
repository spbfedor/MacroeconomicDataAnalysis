from dataclasses import dataclass


@dataclass(frozen=True)
class CountryData:
    country: str
    gdp: float

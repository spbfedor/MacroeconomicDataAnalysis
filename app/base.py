from abc import ABC, abstractmethod
from typing import Callable, Dict, List, Type

from app.schemas import CountryData

REPORT_REGISTRY: Dict[str, Type["BaseReport"]] = {}


def register_report(name: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        REPORT_REGISTRY[name] = func
        return func

    return decorator


class BaseReport(ABC):
    @abstractmethod
    def calculate(self, filenames: List[str]) -> List[CountryData]:
        '''Все отчеты обязаны реализовать этот метод'''
        pass

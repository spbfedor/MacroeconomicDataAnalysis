import pytest
from typing import Callable, List

from macro_reports import average_gdp, CountryData


@pytest.fixture
def temp_csv(tmp_path) -> Callable[[str, List[str]], str]:
    def _create_file(name: str, content: List[str]) -> str:
        file = tmp_path / name
        file.write_text("country,gdp\n" + "\n".join(content))
        return str(file)
    return _create_file


def test_avg_calc(temp_csv: Callable) -> None:
    path: str = temp_csv("data.csv", ["Russia,1000.0", "Russia,2000.0"])

    result: List[CountryData] = average_gdp([path])

    assert result[0].country == "Russia"
    assert result[0].gdp == 1500


def test_sort(temp_csv: Callable) -> None:

    path: str = temp_csv("data.csv", ["small,1000.0", "big,2000.7"])

    result: List[CountryData] = average_gdp([path])

    assert result[0].country == "big"
    assert result[0].gdp == 2000.7
    assert result[1].country == "small"
    assert result[1].gdp == 1000.0


def test_dirty_data(temp_csv: Callable) -> None:
    path: str = temp_csv("data.csv", ["Russia,1000.23", "Fake,zxcv", "USA,"])

    result: List[CountryData] = average_gdp([path])

    assert len(result) == 1
    assert result[0].country == "Russia"
    assert result[0].gdp == 1000.23


def test_missing_file(temp_csv: Callable) -> None:
    path: str = temp_csv("data.csv", ["Russia,1000.23"])

    result: List[CountryData] = average_gdp([path])

    assert len(result) == 1
    assert result[0].country == "Russia"
    assert result[0].gdp == 1000.23

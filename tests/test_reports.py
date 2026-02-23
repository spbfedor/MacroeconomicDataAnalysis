import os

from macro_reports import average_gdp

def create_csv(filename, content):
    with open(filename, 'w', encoding="utf-8") as f:
        f.write("country,gdp\n")
        for i in content:
            f.write(f"{i}\n")

def test_avg_calc():
    test_file = "test_avg.csv"
    create_csv(test_file, ["Russia,1000.0", "Russia,2000.0"])

    result = average_gdp([test_file])

    assert result[0] == ["Russia", 1500.0]
    os.remove(test_file)

def test_sort():
    test_file = "test_sort.csv"
    create_csv(test_file, ["small,1000.0", "big,2000.7"])

    result = average_gdp([test_file])

    assert result[0] == ["big", 2000.7]
    assert result[1] == ["small", 1000.0]
    os.remove(test_file)

def test_dirty_data():
    test_file = "test_dirty.csv"
    create_csv(test_file, ["Russia,1000.23", "Fake,zxcv", "USA,"])

    result = average_gdp([test_file])

    assert len(result) == 1
    assert result[0] == ["Russia", 1000.23]
    os.remove(test_file)

def test_missing_file():
    test_file = "test_dirty.csv"
    create_csv(test_file, ["Russia,1000.23"])

    result = average_gdp([test_file, "test.csv"])

    assert len(result) == 1
    assert result[0] == ["Russia", 1000.23]
    os.remove(test_file)
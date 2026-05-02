import pytest
from i_ink.transform import uvi_to_str, hour_report


@pytest.mark.parametrize("uvi,expected", [
    (0.0,  "Low"),
    (1.9,  "Low"),
    (2.0,  "Moderate"),
    (4.9,  "Moderate"),
    (5.0,  "High"),
    (6.9,  "High"),
    (7.0,  "Very high"),
    (9.9,  "Very high"),
    (10.0, "Extreme"),
    (12.0, "Extreme"),
])
def test_uvi_to_str(uvi, expected):
    assert uvi_to_str(uvi) == expected


def test_hour_report_all_minutes_in_past():
    # All timestamps are in the past — future_minutes will be empty
    past_minutes = [{"dt": 1, "precipitation": 0.0} for _ in range(60)]
    result = hour_report(past_minutes)
    assert isinstance(result, str)

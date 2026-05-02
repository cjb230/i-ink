import pytest
import json
from datetime import time
from pathlib import Path
from freezegun import freeze_time
from i_ink.transform import uvi_to_str, hour_report, transform_trains, transform_weather


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


@freeze_time("2025-01-01 08:00:00")
def test_transform_trains_max_display():
    trains_data = {
        "warsaw":        [(time(8, 5), "1001"), (time(8, 10), "1002"), (time(8, 15), "1003"), (time(8, 20), "1004"), (time(8, 25), "1005")],
        "podkowa_lesna": [(time(8, 5), "2001"), (time(8, 10), "2002"), (time(8, 15), "2003"), (time(8, 20), "2004"), (time(8, 25), "2005")],
        "timestamp": "2025-01-01T08:00:00+00:00",
    }
    result = transform_trains(trains_data, max_display=3)
    assert len(result["warsaw"]) <= 3
    assert len(result["podkowa_lesna"]) <= 3


@freeze_time("2025-07-13T08:34:08.557943+00:00")
def test_transform_weather_missing_minutely():
    data = json.loads(Path("tests/data/alert_status.txt").read_text(encoding="utf-8"))
    del data["result"]["minutely"]
    result = transform_weather(data)
    assert "No minute-by-minute data" in result["current"]["text_lines"]


@freeze_time("2025-01-01 23:55:00")
def test_transform_trains_includes_post_midnight_trains():
    # At 23:55, trains at 00:05 and 00:12 are only 10-17 minutes away
    # and should appear, not be filtered out by a naive time comparison
    trains_data = {
        "warsaw": [(time(0, 5), "1001"), (time(0, 12), "1002")],
        "podkowa_lesna": [],
        "timestamp": "2025-01-01T23:55:00+00:00",
    }
    result = transform_trains(trains_data)
    assert len(result["warsaw"]) == 2


def test_hour_report_all_minutes_in_past():
    # All timestamps are in the past — future_minutes will be empty
    past_minutes = [{"dt": 1, "precipitation": 0.0} for _ in range(60)]
    result = hour_report(past_minutes)
    assert isinstance(result, str)

from datetime import datetime
from i_ink.weather import format_forecast_entry


def test_format_forecast_entry():
    entry = (datetime(2021, 1, 1, 0, 0), 15, 20, 10)
    result = format_forecast_entry(entry)
    assert "2021-01-01 00:00:00" in result
    assert "15°C" in result
    assert "Clouds: 20%" in result
    assert "Rain Probability: 10%" in result

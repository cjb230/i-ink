from datetime import datetime
from unittest.mock import patch
from i_ink.weather import fetch_hourly_forecast, extract_short_term_forecast, format_forecast_entry

def test_fetch_hourly_forecast():
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'hourly': []}
        result = fetch_hourly_forecast(0, 0)
        assert isinstance(result, dict)
        mock_get.assert_called_once()

def test_extract_short_term_forecast():
    data = {
        'hourly': [
            {'dt': 1609459200, 'temp': 15.5, 'clouds': 20, 'pop': 0.1},
            {'dt': 1609462800, 'temp': 16.5, 'clouds': 30, 'pop': 0.2},
            {'dt': 1609466400, 'temp': 17.5, 'clouds': 40, 'pop': 0.3}
        ]
    }
    result = extract_short_term_forecast(data)
    assert len(result) == 3
    assert isinstance(result[0], tuple)

def test_format_forecast_entry():
    entry = (datetime(2021, 1, 1, 0, 0), 15, 20, 10)
    result = format_forecast_entry(entry)
    assert "2021-01-01 00:00:00" in result
    assert "15°C" in result
    assert "Clouds: 20%" in result
    assert "Rain Probability: 10%" in result

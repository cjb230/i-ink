from pathlib import Path
from datetime import datetime
import pytest
import json
from freezegun import freeze_time
import pytesseract
from PIL import Image

from i_ink.transform import transform_weather
from i_ink.weather import format_forecast_entry
from i_ink.render import render_weather_now

@pytest.fixture
def alert_json():
    path = Path("tests/data/alert_status.txt")
    return json.loads(path.read_text(encoding="utf-8"))


def test_format_forecast_entry():
    entry = (datetime(2021, 1, 1, 0, 0), 15, 20, 10)
    result = format_forecast_entry(entry)
    assert "2021-01-01 00:00:00" in result
    assert "15°C" in result
    assert "Clouds: 20%" in result
    assert "Rain Probability: 10%" in result


@freeze_time("2025-07-13T08:34:08.557943+00:00")
def test_alerts(alert_json):
    # Is alert in dict passed to rendering?
    weather_dict = transform_weather(alert_json)
    assert "Yellow Thunderstorm warning" ==  weather_dict["current"]["alert_str"]
    # Is alert text rendered correctly?
    img = render_weather_now(weather_dict["current"])
    img = img.crop((256, 0, 480, 250))  # Crop to the area where the alert should be
    text = pytesseract.image_to_string(img, lang="eng")
    print(text)
    assert "Yellow Thunderstorm warning" in text
    
from pathlib import Path
from datetime import datetime
import pytest
import json
from freezegun import freeze_time
import pytesseract
from PIL import Image

from i_ink.transform import transform_weather
from i_ink.render import render_weather_now

@pytest.fixture
def alert_json():
    path = Path("tests/data/alert_status.txt")
    return json.loads(path.read_text(encoding="utf-8"))


@freeze_time("2025-07-13T08:34:08.557943+00:00")
def test_alerts(alert_json):
    # Is alert in dict passed to rendering?
    weather_dict = transform_weather(alert_json)
    assert "Yellow Thunderstorm warning" ==  weather_dict["current"]["alert_str"]
    # Is alert text rendered correctly?
    img = render_weather_now(weather_dict["current"])
    img = img.crop((256, 0, 480, 250))  # Crop to the area where the alert should be
    text = pytesseract.image_to_string(img, lang="eng")
    assert "Yellow Thunderstorm" in text
    assert "warning" in text

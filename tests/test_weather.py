from pathlib import Path
import pytest
import json
from freezegun import freeze_time
import pytesseract
from PIL import Image

from i_ink.transform import transform_weather
from i_ink.render import render_weather_now, render_all

@pytest.fixture
def alert_json():
    path = Path("tests/data/alert_status.txt")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("bad_weather", [
    {"timestamp": "2025-01-01T08:00:00+00:00", "error": "upstream API error"},
    {"timestamp": "2025-01-01T08:00:00+00:00"},  # missing "result" key
])
def test_render_all_survives_weather_error(bad_weather):
    transformed_weather = transform_weather(bad_weather)
    transformed_trains = {"warsaw": [], "podkowa_lesna": []}
    result = render_all(transformed_trains, transformed_weather, "08:00:00")
    assert isinstance(result, Image.Image)


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

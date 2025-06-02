from PIL import Image

from .display import update_screen
from .trains import get_next_wkd_trains, filter_trains_for_display
from .render import render_all
from .transform import transform_weather, transform_trains
from .weather import fetch_forecast


def collect_all_data():
    raw_trains = get_next_wkd_trains()
    raw_weather_forecast = fetch_forecast()
    return {
        "trains": raw_trains,
        "weather": raw_weather_forecast
    }


def run_all():
    data = collect_all_data()
    transformed_weather = transform_weather(data["weather"])
    transformed_trains = transform_trains(data["trains"])
    result_image: Image = render_all(transformed_trains, transformed_weather)
    update_screen(result_image)

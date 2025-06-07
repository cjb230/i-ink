import time
from PIL import Image

from .display import conditional_update_screen
from .trains import get_next_wkd_trains
from .render import render_all
from .transform import transform_weather, transform_trains
from .weather import fetch_forecast


SLEEP_DURATION_S = 240


def collect_all_data():
    raw_trains = get_next_wkd_trains()
    raw_weather_forecast = fetch_forecast()
    return {
        "trains": raw_trains,
        "weather": raw_weather_forecast
    }


def run_all():
    n = 1
    while True:
        print(f"Starting run {n}")
        data = collect_all_data()
        transformed_weather = transform_weather(data["weather"])
        transformed_trains = transform_trains(data["trains"])
        train_timestamp = transformed_trains["update_str"]
        del transformed_trains["update_str"]
        result_image: Image = render_all(transformed_trains, transformed_weather, train_timestamp)
        conditional_update_screen(result_image)
        result_image.save("all.png")
        n += 1
        print(f"Sleeping for {SLEEP_DURATION_S} seconds at {time.localtime()} .\n")
        time.sleep(SLEEP_DURATION_S)

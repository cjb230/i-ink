import atexit
import os
import signal
import sys
import time
from PIL import Image
# from . import epd7in5_V2

from .display import get_display

from .trains import get_next_wkd_trains
from .render import render_all
from .transform import transform_weather, transform_trains
from .weather import fetch_forecast


SLEEP_DURATION_S = 240
FAILURE_ALERT_THRESHOLD = int(os.getenv("I_INK_FAILURE_ALERT_THRESHOLD", "3"))
DISPLAY = get_display()
PREVIOUS_IMAGE_BODY: Image = Image.new("RGB", (480, 750), "white")
LATEST_WEATHER = None
LATEST_TRAINS = None
WEATHER_FAILURE_COUNT = 0
TRAINS_FAILURE_COUNT = 0
LAST_WEATHER_ERROR = None
LAST_TRAINS_ERROR = None


def cleanup():
    DISPLAY.clear()


def handle_signal(signum, frame):
    atexit.unregister(cleanup)
    cleanup()
    sys.exit(0)


atexit.register(cleanup)
signal.signal(signal.SIGINT, handle_signal)  # Ctrl+C
signal.signal(signal.SIGTERM, handle_signal) 


def conditional_update_screen(image: Image):
    global PREVIOUS_IMAGE_BODY
    new_image_body = image.crop((0, 0, 480, 750))
    if new_image_body.tobytes() != PREVIOUS_IMAGE_BODY.tobytes():
        print("Image changed, updating screen")
        DISPLAY.clear()
        DISPLAY.show(image)
        PREVIOUS_IMAGE_BODY = new_image_body
    else:
        print("Image unchanged, not updating screen")
    return


def error_message(source_name: str, failure_count: int, last_error: str) -> str:
    return (
        f"{source_name} failed {failure_count} times in a row. "
        f"Run on 192.168.1.66: tail /home/cjb/i-ink.log. "
        f"Last error: {last_error or 'unknown'}"
    )


def fetch_weather_for_display():
    global LATEST_WEATHER, WEATHER_FAILURE_COUNT, LAST_WEATHER_ERROR
    try:
        raw_weather_forecast = fetch_forecast()
        transformed_weather = transform_weather(raw_weather_forecast)
        if "error" in transformed_weather:
            raise ValueError(transformed_weather["error"])
        LATEST_WEATHER = transformed_weather
        WEATHER_FAILURE_COUNT = 0
        LAST_WEATHER_ERROR = None
    except Exception as e:
        WEATHER_FAILURE_COUNT += 1
        LAST_WEATHER_ERROR = str(e)
        print(f"Weather source failed ({WEATHER_FAILURE_COUNT} in a row): {e}")

    if WEATHER_FAILURE_COUNT > FAILURE_ALERT_THRESHOLD:
        return {
            "update_str": LATEST_WEATHER["update_str"] if LATEST_WEATHER else "never",
            "error": error_message("Weather source", WEATHER_FAILURE_COUNT, LAST_WEATHER_ERROR),
        }
    if LATEST_WEATHER:
        return LATEST_WEATHER
    return {"update_str": "never", "missing": True}


def fetch_trains_for_display():
    global LATEST_TRAINS, TRAINS_FAILURE_COUNT, LAST_TRAINS_ERROR
    try:
        raw_trains = get_next_wkd_trains()
        LATEST_TRAINS = transform_trains(raw_trains)
        TRAINS_FAILURE_COUNT = 0
        LAST_TRAINS_ERROR = None
    except Exception as e:
        TRAINS_FAILURE_COUNT += 1
        LAST_TRAINS_ERROR = str(e)
        print(f"Train source failed ({TRAINS_FAILURE_COUNT} in a row): {e}")

    if TRAINS_FAILURE_COUNT > FAILURE_ALERT_THRESHOLD:
        return {
            "warsaw": [],
            "podkowa_lesna": [],
            "update_str": LATEST_TRAINS["update_str"] if LATEST_TRAINS else "never",
            "error": error_message("Train source", TRAINS_FAILURE_COUNT, LAST_TRAINS_ERROR),
        }
    if LATEST_TRAINS:
        return LATEST_TRAINS
    return {"warsaw": [], "podkowa_lesna": [], "update_str": "never", "missing": True}


def run_all():
    n = 1
    while True:
        try:
            print(f"Starting run {n}")
            n += 1
            transformed_trains = fetch_trains_for_display()
            transformed_weather = fetch_weather_for_display()
            train_timestamp = transformed_trains["update_str"]
            result_image: Image = render_all(transformed_trains, transformed_weather, train_timestamp)
            conditional_update_screen(result_image)
            result_image.save("all.png")
            print(f"Sleeping for {SLEEP_DURATION_S} seconds at {time.localtime()} .\n")
            time.sleep(SLEEP_DURATION_S)
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Sleeping for 60 seconds before retrying...")
            time.sleep(60)
            continue

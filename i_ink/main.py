import time
import atexit
import signal
import sys
from PIL import Image, ImageDraw
from gpiozero import Device
# from . import epd7in5_V2

from .display import get_display

from .trains import get_next_wkd_trains, filter_trains_for_display
from .render import render_all
from .transform import transform_weather, transform_trains
from .weather import fetch_forecast


SLEEP_DURATION_S = 240
DISPLAY = get_display()
PREVIOUS_IMAGE_BODY: Image = Image.new("RGB", (480, 750), "white")


def cleanup():
    DISPLAY.clear()


def handle_signal(signum, frame):
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
        DISPLAY.show(image)
        PREVIOUS_IMAGE_BODY = new_image_body
    else:
        print("Image unchanged, not updating screen")
    return


def collect_all_data():
    raw_trains = get_next_wkd_trains()
    raw_weather_forecast = fetch_forecast()
    return {
        "trains": raw_trains,
        "weather": raw_weather_forecast
    }


def run_display_update():
    data = collect_all_data()
    print("Data collected.")
    # print(data["weather"])
    result_image: Image = render_all(data["trains"], data["weather"])
    #result_image.save("xyz.png")
    print("Rendering done, sending to screen")
    """epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    buf = epd.getbuffer(result_image)
    epd.display(buf)
    print("Sent to screen")
    Device.pin_factory.close()
    print("pin factory closed")
    exit()
    """


def run_all():
    n = 1
    while True:
        try:
            print(f"Starting run {n}")
            n += 1
            data = collect_all_data()
            transformed_weather = transform_weather(data["weather"])
            transformed_trains = transform_trains(data["trains"])
            train_timestamp = transformed_trains["update_str"]
            del transformed_trains["update_str"]
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
        finally:
            cleanup()

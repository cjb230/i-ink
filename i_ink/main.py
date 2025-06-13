from PIL import Image, ImageDraw
from gpiozero import Device
from . import epd7in5_V2

from .trains import get_next_wkd_trains, filter_trains_for_display
from .render import render_all
from .weather import get_short_term_forecast


def collect_all_data():
    raw_trains = get_next_wkd_trains()
    trains_to_show = filter_trains_for_display(raw_trains)

    raw_weather_forecast = get_short_term_forecast(hours=3)
    # print(f"rwf = {raw_weather_forecast}")
    return {
        "trains": trains_to_show,
        "weather": raw_weather_forecast
    }

def run_display_update():
    data = collect_all_data()
    print("Data collected.")
    # print(data["weather"])
    result_image: Image = render_all(data["trains"], data["weather"])
    #result_image.save("xyz.png")
    print("Rendering done, sending to screen")
    epd = epd7in5_V2.EPD()
    epd.init()
    epd.Clear()
    buf = epd.getbuffer(result_image)
    epd.display(buf)
    print("Sent to screen")
    Device.pin_factory.close()
    print("pin factory closed")
    exit()




def run_debug_mode():
    data = collect_all_data()
    print("\nTrain departures:")
    for t, n in data["trains"]:
        print(f"{t.strftime('%H:%M')} — train {n}")

    print("\nShort-term forecast:")
    for line in data["weather"]:
        print(line)

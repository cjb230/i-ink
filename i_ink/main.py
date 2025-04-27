from .trains import get_next_wkd_trains, filter_trains_for_display
from .render import render_train_info_image
from .weather import get_short_term_forecast

def collect_all_data():
    raw_trains = get_next_wkd_trains()
    trains_to_show = filter_trains_for_display(raw_trains)

    # Example coordinates (Warsaw); these should be configurable
    lat, lon = 52.2297, 21.0122
    weather_forecast = get_short_term_forecast(lat, lon, hours=3)

    return {
        "trains": trains_to_show,
        "weather": weather_forecast
    }

def run_display_update():
    data = collect_all_data()
    render_train_info_image(data["trains"])

def run_debug_mode():
    data = collect_all_data()
    print("\nTrain departures:")
    for t, n in data["trains"]:
        print(f"{t.strftime('%H:%M')} — train {n}")

    print("\nShort-term forecast:")
    for line in data["weather"]:
        print(line)

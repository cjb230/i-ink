from datetime import datetime, timedelta
import zoneinfo

def printable_hour(unix_time: int) -> str:
    local_time = datetime.fromtimestamp(unix_time)
    return "24" if local_time.hour == 0 else str(local_time.hour)


def transform_weather(weather_data) -> dict:
    results = {}
    results["hourly"] = weather_data["result"]["hourly"][1:5]
    for hour in results["hourly"]:
        hour["hour_str"] = printable_hour(unix_time=hour["dt"])
        del hour["dt"]
    results["update_str"] = weather_data["timestamp"]

    dt_utc = datetime.fromisoformat(weather_data["timestamp"])
    time_str = dt_utc.astimezone(zoneinfo.ZoneInfo("Europe/Warsaw")).strftime("%H:%M:%S")
    results["update_str"] = time_str
    return results


def transform_trains(trains_data, max_display=3, earliest_minutes_ahead=1) -> dict:
    now = datetime.now().time()
    results = {"warsaw": [],  "podkowa_lesna": []}

    timestamp_str = trains_data["timestamp"]
    del trains_data["timestamp"]

    #print(train_dict)
    for train_direction, train_list in trains_data.items():
        for train_time, train_no in train_list:
            if train_time > now:
                delta = datetime.combine(datetime.today(), train_time) - datetime.combine(datetime.today(), now)
                if delta >= timedelta(minutes=earliest_minutes_ahead):
                    results[train_direction].append((train_time, train_no))
                if len(results) == max_display:
                    break

    dt_utc = datetime.fromisoformat(timestamp_str)
    results["update_str"] = dt_utc.astimezone(zoneinfo.ZoneInfo("Europe/Warsaw")).strftime("%H:%M:%S")

    return results
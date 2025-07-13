from PIL import Image
from i_ink.render import render_all
from i_ink.transform import transform_weather, transform_trains
from i_ink.main import collect_all_data
 
# raw_weather_forecast = get_short_term_forecast(hours=4)
# x = render_weather_hours_image(weather, output_to_file=True, output_height=100, output_width=480, output_path="weather_hours.png")
# print("Fetching...")
# raw_weather_forecast = get_short_term_forecast(hours=4)
# print(len(raw_weather_forecast))
# fc = fetch_forecast()
# print("Fetched.")
# four_hours_fc = get_hours_forecast(complete_forecast=fc["result"], hours=4)
# x = render_weather_hours_image(four_hours_fc, output_to_file=True, output_height=150, output_width=480, output_path="weather_hours.png")
data = collect_all_data()
transformed_weather = transform_weather(data["weather"])
transformed_trains = transform_trains(data["trains"])

# x = render_weather_hours_image(transformed_weather, output_to_file=True, output_height=100, output_width=480, output_path="weather_hours.png")
# x.save("weather_hours.png")
train_timestamp = transformed_trains["update_str"]
del transformed_trains["update_str"]
result_image: Image = render_all(transformed_trains, transformed_weather, train_timestamp )

result_image.save("all.png")

from i_ink.render import render_weather_hour
x = render_weather_hour(weather_data={"dt": 1747936800, "temp": 284.94, "feels_like": 284.47, "pressure": 1006, "humidity": 88, "dew_point": 283.02, "uvi": 0, "clouds": 20, "visibility": 10000, "wind_speed": 2.52, "wind_deg": 267, "wind_gust": 4.93, "weather": [{"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}], "pop": 0.2, "rain": {"1h": 1.33}}, output_to_file=True)


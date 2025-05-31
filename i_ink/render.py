import os
import cairosvg
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# enum for size
# ICON_SIZE: 


# Get path to the directory where run.py is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"base dir = {BASE_DIR}")
FONT_PATH = os.path.join(BASE_DIR, "times_new_roman.ttf")
print(f"font path = {FONT_PATH}")
ICON_IMAGE_BASE_PATH = os.path.join(BASE_DIR, "svg")

#wkd_png = os.path.join(base_dir, "wkd.png")
#wkd_overlay = Image.open(wkd_png).convert("RGBA")
try:
    FONT = ImageFont.truetype(font=FONT_PATH, size=35)
except IOError:
    FONT = ImageFont.load_default()

NAME_MAP = {"warsaw": "Warsaw","podkowa_lesna": "Podkowa Leśna"}

def render_train_info_image(all_trains, output_to_file=False, width=800, height=150, output_path="train_times.png"):
    """
    Renders a white background image with train times in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
     #image.paste(wkd_overlay, (50, 50))

    draw.text((10, 0), "Next WKD Trains:", font=FONT, fill="black")

    y = 35
    x = 30
    for direction, trains in all_trains.items():
        draw.text((x, y), f"To {NAME_MAP[direction]}:", font=FONT, fill="black")
        y += 35
        x += 30
        z = 0
        for time, train_no in trains:
            font = ImageFont.truetype(font=FONT_PATH, size=23)
            z += 1
            line = f"{time.strftime('%H:%M')}"  # — ({train_no})"
            draw.text((x, y), line, font=font, fill="black")
            y += 25
            if z > 2:
                y = 30
                break
        x += 410

    if output_to_file:
        image.save(output_path)
    return image



def icon_image_path() -> str:
    path = os.path.join(ICON_IMAGE_BASE_PATH, "01d_w.png")
    return path


def render_svg_to_pillow(svg_path: str, scale: float = 1.0) -> Image.Image:
    # Read the SVG file
    print(f"Rendering {str(svg_path)}")
    with open(svg_path, "rb") as f:
        svg_data = f.read()

    # Convert SVG to PNG bytes, scaling via DPI
    png_bytes = cairosvg.svg2png(bytestring=svg_data, scale=scale)

    # Load PNG bytes into a Pillow image
    # return Image.open(BytesIO(png_bytes)).convert("1")  # convert to 1-bit monochrome
    return Image.open(BytesIO(png_bytes)).convert("RGBA")


"""
{"dt": 1747936800, "temp": 284.94, "feels_like": 284.47, "pressure": 1006, "humidity": 88, "dew_point": 283.02, "uvi": 0, "clouds": 20, "visibility": 10000, "wind_speed": 2.52, "wind_deg": 267, "wind_gust": 4.93, "weather": [{"id": 501, "main": "Rain", "description": "moderate rain", "icon": "10d"}], "pop": 0.2, "rain": {"1h": 1.33}}
{"dt": 1747940400, "temp": 285.24, "feels_like": 284.8, "pressure": 1006, "humidity": 88, "dew_point": 283.32, "uvi": 0, "clouds": 36, "visibility": 9637, "wind_speed": 1.43, "wind_deg": 258, "wind_gust": 3.23, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}], "pop": 1, "rain": {"1h": 1}}
{"dt": 1747944000, "temp": 285.31, "feels_like": 284.91, "pressure": 1006, "humidity": 89, "dew_point": 283.55, "uvi": 0, "clouds": 52, "visibility": 6104, "wind_speed": 1.99, "wind_deg": 271, "wind_gust": 5.13, "weather": [{"id": 500, "main": "Rain", "description": "light rain", "icon": "10n"}], "pop": 1, "rain": {"1h": 0.24}}
"""
def render_weather_hour(weather_data: dict, width: int=100, height: int=100, icon_size: int=2, output_path: str ="weather_hour.png", output_to_file: bool=False) -> Image:
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    # hour = 
    icon_index: str = weather_data["weather"][0]["icon"]
    icon_file_name_1 = icon_index + ".svg"
    # icon_file_name_2 = icon_index + "_w.png"

    # print(f"icon index = {icon_index}")
    temp: int = round(weather_data["temp"] - 273.15)
    draw.text((10, 0), "06", font=FONT, fill="black")
    icon_path_1 = os.path.join(ICON_IMAGE_BASE_PATH, icon_file_name_1)
    # icon_path_2 = os.path.join(ICON_IMAGE_BASE_PATH, icon_file_name_2)
    print(f"icon_path={icon_path_1}")
    # icon_image_1 = Image.open(icon_path_1)
    icon_image_1 = render_svg_to_pillow(icon_path_1, scale=0.5)
    # icon_image_2 = Image.open(icon_path_2)
    image.paste(icon_image_1, (0,0),icon_image_1)
    draw.text((10, 0), str(temp), font=FONT, fill="black")

    if output_to_file:
        image.save(output_path)
    return image    


def render_weather_image(weather_data, output_to_file=False, width=800, height=650, output_path="weather.png") -> Image:
    """
    Renders a white background image with weather in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
     #image.paste(wkd_overlay, (50, 50))

    # Load font
    try:
        font = ImageFont.truetype(font=FONT_PATH, size=35)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 0), "Weather:", font=font, fill="black")

    y = 35
    x = 30
    print(weather_data)
    for hour in weather_data:
        font = ImageFont.truetype(font=FONT_PATH, size=30)
        draw.text((x, y), f"{hour['time']}: {hour['temperature']}", font=font, fill="black")
        y += 35

    if output_to_file:
        image.save(output_path)
    return image


def render_all(trains_data, weather_data, output_path="final.png") -> Image:
    train_part = render_train_info_image(trains_data)
    weather_part = render_weather_image(weather_data)
    #new_img = Image.new("RGB", (max(img1.width, img2.width), img1.height + img2.height))
    new_img = Image.new("RGB", (800, 480))

    new_img.paste(train_part, (0, 0))
    new_img.paste(weather_part, (0, 120))
    # new_img.save(output_path)
    return new_img

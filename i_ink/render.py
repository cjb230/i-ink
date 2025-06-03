import os
import cairosvg
from datetime import datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


# Get path to the directory where run.py is located
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# FONT_PATH = os.path.join(BASE_DIR, "times_new_roman.ttf")
FONT_PATH = os.path.join(BASE_DIR, "amazon_ember_display_light.ttf")
ICON_IMAGE_BASE_PATH = os.path.join(BASE_DIR, "svg")
LOCAL_TZ = datetime.now().astimezone().tzinfo

# print(f"base dir = {BASE_DIR}")
# print(f"font path = {FONT_PATH}")
# print(f"ICON_IMAGE_BASE_PATH = {ICON_IMAGE_BASE_PATH}")
# print(f"local tz = {LOCAL_TZ}")

try:
    LARGE_FONT = ImageFont.truetype(font=FONT_PATH, size=32)
    MEDIUM_FONT = ImageFont.truetype(font=FONT_PATH, size=23)
    TINY_FONT = ImageFont.truetype(font=FONT_PATH, size=12)    
except IOError as ioe:
    print(f"Could not load typeface!\n{ioe}")
    LARGE_FONT = ImageFont.load_default()
    MEDIUM_FONT = LARGE_FONT
    TINY_FONT = LARGE_FONT

NAME_MAP = {"warsaw": "Warsaw","podkowa_lesna": "Podkowa Leśna"}

def render_train_info_image(all_trains, output_to_file=False, width=480, height=150, output_path="train_times.png"):
    """
    Renders a white background image with train times in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
     #image.paste(wkd_overlay, (50, 50))

    draw.text((82, 0), "Next WKD Trains To:", font=LARGE_FONT, fill="black")

    title_y = 35
    start_y = 31
    y = start_y
    location_underline_y = 59
    for direction, trains in all_trains.items():
        z = 0
        if NAME_MAP[direction] == "Warsaw":
            title_x = 62
            time_x = 70
        else:
            title_x = 260
            time_x = 310
        draw.text((title_x, title_y), f"{NAME_MAP[direction]}", font=MEDIUM_FONT, fill="black")
        y += 30
        if NAME_MAP[direction] == "Warsaw":
            draw.line([(title_x-1, location_underline_y), (title_x + 80, location_underline_y)], fill="black", width=1)
        else:
            draw.line([(title_x-1, location_underline_y), (title_x + 158, location_underline_y)], fill="black", width=1)            
        for time, train_no in trains:
            z += 1
            print(f"y = {y}")
            line = f"{time.strftime('%H:%M')}"  # — ({train_no})"
            draw.text((time_x, y), line, font=MEDIUM_FONT, fill="black")
            y += 27
            if z > 2:
                y = start_y
                break

    if output_to_file:
        image.save(output_path)
    return image



def render_svg_to_pillow(svg_path: str, scale: float = 1.0) -> Image.Image:
    # Read the SVG file
    print(f"Rendering {str(svg_path)}")
    with open(svg_path, "rb") as f:
        svg_data = f.read()

    # Convert SVG to PNG bytes, scaling via DPI
    png_bytes = cairosvg.svg2png(bytestring=svg_data, scale=scale)

    return Image.open(BytesIO(png_bytes)).convert("RGBA")


def render_weather_hour(weather_data: dict, width: int=100, height: int=100, icon_size: int=2, output_path: str ="weather_hour.png", output_to_file: bool=False) -> Image:
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    icon_index: str = weather_data["weather"][0]["icon"]
    icon_file_name_1 = icon_index + ".svg"

    temp_str: str = str(round(weather_data["temp"] - 273.15)) + '°C'
    # hour_str = printable_hour(unix_time=weather_data["dt"])

    icon_path_1 = os.path.join(ICON_IMAGE_BASE_PATH, icon_file_name_1)
    print(f"icon_path={icon_path_1}")
    draw.text((35, 0), weather_data["hour_str"], font=MEDIUM_FONT, fill="black")
    icon_image_1 = render_svg_to_pillow(icon_path_1, scale=0.08)
    image.paste(icon_image_1, (28,26),icon_image_1)
    print(f"temp = {temp_str}")
    draw.text((19, 63), str(temp_str), font=LARGE_FONT, fill="black")

    if output_to_file:
        image.save(output_path)
    return image    


def render_weather_hours_image(weather_data, output_to_file=False, output_height=150, output_width=480, panel_height=100, panel_width=100, output_path="weather_hours.png") -> Image:
    """
    Renders a white background image with weather in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (output_width, output_height), "white")

    total_hours = len(weather_data)
    total_panel_width = total_hours * panel_width
    spare_width = output_width - total_panel_width
    vertical_spacing = int(spare_width / (total_hours+1))

    spare_height = output_height - panel_height

    x = vertical_spacing
    y = int(spare_height / 2)
    for hour in weather_data:
        image.paste(render_weather_hour(hour, output_to_file=True), (x, y))
        x += panel_width + vertical_spacing

    if output_to_file:
        image.save(output_path)
    return image


def render_weather_now(weather_data, output_to_file=False, output_height=250, output_width=480, output_path="weather_now.png") -> Image:
    image = Image.new("RGB", (output_width, output_height), "white")
    
    return image


def render_weather_days(weather_data, output_to_file=False, output_height=200, output_width=480, output_path="weather_now.png") -> Image:
    image = Image.new("RGB", (output_width, output_height), "white")
    return image


def render_footer(weather_updated_time: str, trains_updated_time: str, motd: str,
                  output_to_file=False, output_height=50, output_width=480, output_path="footer.png"
                                    ) -> Image.Image:
    footer_img = Image.new("RGB", (output_width, output_height), "white")
    draw = ImageDraw.Draw(footer_img)
    draw.text((10, 10), "Weather updated:", font=TINY_FONT, fill="black")

    draw.text((10, 25), f"  {weather_updated_time}", font=TINY_FONT, fill="black")
    draw.text((240, 10), "Trains updated:", font=TINY_FONT, fill="black")
    draw.text((240, 25), f"  {trains_updated_time}", font=TINY_FONT, fill="black")
     
    """draw.text((240, 10), f"{motd}", font=TINY_FONT, fill="black")"""
    if output_to_file:
        footer_img.save(output_path)
    return footer_img


def render_all(transformed_trains, transformed_weather, train_timestamp, output_to_file=False, output_path="final.png") -> Image:
    train_part = render_train_info_image(transformed_trains)
    weather_hours = render_weather_hours_image(transformed_weather["hourly"])
    footer = render_footer(transformed_weather["update_str"], train_timestamp, motd="Hello World!", output_to_file=True)
    weather_days = render_weather_days(transformed_weather)
    weather_now = render_weather_now(transformed_weather)

    new_img = Image.new("RGB", (480, 800))
    new_img.paste(weather_now, (0,0))
    new_img.paste(weather_hours, (0, 250))
    new_img.paste(weather_days, (0, 400))
    new_img.paste(train_part, (0, 600))
    new_img.paste(footer, (0, 750))
    if output_to_file:
        new_img.save(output_path)
    return new_img

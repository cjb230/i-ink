import os
from PIL import Image, ImageDraw, ImageFont

# Get path to the directory where run.py is located
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f"base dir = {base_dir}")
font_path = os.path.join(base_dir, "times_new_roman.ttf")
print(f"font path = {font_path}")
#wkd_png = os.path.join(base_dir, "wkd.png")
#wkd_overlay = Image.open(wkd_png).convert("RGBA")

NAME_MAP = {"warsaw": "Warsaw","podkowa_lesna": "Podkowa Leśna"}

def render_train_info_image(all_trains, output_to_file=False, width=800, height=150, output_path="train_times.png"):
    """
    Renders a white background image with train times in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
     #image.paste(wkd_overlay, (50, 50))

    # Load font
    font = ImageFont.truetype(font=font_path, size=35)
    # font = ImageFont.load_default()

    draw.text((10, 0), "Next WKD Trains:", font=font, fill="black")

    y = 35
    x = 30
    for direction, trains in all_trains.items():
        font = ImageFont.truetype(font=font_path, size=30)
        draw.text((x, y), f"To {NAME_MAP[direction]}:", font=font, fill="black")
        y += 35
        x += 30
        z = 0
        for time, train_no in trains:
            font = ImageFont.truetype(font=font_path, size=23)
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


def render_weather_image(weather_data, output_to_file=False, width=800, height=650, output_path="weather.png"):
    """
    Renders a white background image with weather in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
     #image.paste(wkd_overlay, (50, 50))

    # Load font
    try:
        font = ImageFont.truetype(font=font_path, size=35)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 0), "Weather:", font=font, fill="black")

    y = 35
    x = 30
    print(weather_data)
    for hour in weather_data:
        font = ImageFont.truetype(font=font_path, size=30)
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
    print("Image pasted.")
    return new_img

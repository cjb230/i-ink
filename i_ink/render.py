from PIL import Image, ImageDraw, ImageFont

def render_train_info_image(trains, output_path="train_times.png", width=250, height=122):
    """
    Renders a white background image with train times in black text.
    Output is saved to the given path.
    """
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # Load font
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    draw.text((10, 5), "Next WKD trains:", font=font, fill="black")

    y = 30
    for time, train_no in trains:
        line = f"{time.strftime('%H:%M')} — train {train_no}"
        draw.text((10, y), line, font=font, fill="black")
        y += 22

    image.save(output_path)
from PIL import Image
from gpiozero import Device

# from . import epd7in5_V2


def update_screen(image: Image):
    """
    epd = epd7in5_V2.EPD()
    epd.init()
    buf = epd.getbuffer(image)
    epd.display(buf)
    Device.pin_factory.close()
    """
    return

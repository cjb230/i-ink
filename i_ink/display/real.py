from display.interface import DisplayInterface

class RealDisplay(DisplayInterface):
    def __init__(self):
        # Import hardware libs only when instantiating RealDisplay
        try:
            import epd7in5_V2
            import RPi.GPIO as GPIO
        except ImportError as e:
            raise ImportError(f"RealDisplay unavailable: {e}")
        self.epd = epd7in5_V2.EPD()
        self.epd.init()
    def show(self, image):
        buf = self.epd.getbuffer(image)
        self.epd.display(buf)
    def sleep(self):
        self.epd.sleep()
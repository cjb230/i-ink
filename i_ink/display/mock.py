from .interface import DisplayInterface

class MockDisplay(DisplayInterface):
    def __init__(self, out_path="out.png"):
        self.out_path = out_path

    def init(self):
        pass

    def show(self, image):
        # e.g. save or display image
        image.save(self.out_path)
        image.show()

    def sleep(self):
        pass

    def clear(self):
        pass
    
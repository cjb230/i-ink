import platform
from .interface import DisplayInterface

def is_raspberry_pi() -> bool:
    return platform.system() == "Linux" and "raspberrypi" in platform.uname().nodename.lower()

if is_raspberry_pi():
    print("Detected Raspberry Pi. Using real display class.")
    from .real import RealDisplay
    _DisplayClass = RealDisplay
else:
    print("Not a Raspberry Pi. Using mock display class.")
    from .mock import MockDisplay
    _DisplayClass = MockDisplay

def get_display(*args, **kwargs) -> DisplayInterface:
    return _DisplayClass(*args, **kwargs)

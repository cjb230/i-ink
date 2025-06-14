from .interface import DisplayInterface

try:
    from .real import RealDisplay
    _DisplayClass = RealDisplay
    print("Using real display class.")
except ImportError:
    print("Could not import real display class.\nImporting mock display class instead...")
    from .mock import MockDisplay
    _DisplayClass = MockDisplay

def get_display(*args, **kwargs) -> DisplayInterface:
    return _DisplayClass(*args, **kwargs)

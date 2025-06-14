from .interface import DisplayInterface

try:
    from .real import RealDisplay
    _DisplayClass = RealDisplay
except ImportError:
    from .mock import MockDisplay
    _DisplayClass = MockDisplay

def get_display(*args, **kwargs) -> DisplayInterface:
    return _DisplayClass(*args, **kwargs)

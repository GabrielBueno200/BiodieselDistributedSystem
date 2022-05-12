import threading
from typing import Any, Callable


def set_interval(callback: Callable[[Any], None], secs):
    """
    Calls a callback function at specified intervals given by ms 
    """
    def func_wrapper():
        set_interval(callback, secs)
        callback()
    t = threading.Timer(secs, func_wrapper)
    t.start()
    return t

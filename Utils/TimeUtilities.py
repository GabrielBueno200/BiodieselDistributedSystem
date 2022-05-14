import threading
from typing import Any, Callable


def set_interval(callback: Callable[[Any], None], secs: float):
    """
    Calls a callback function at specified intervals given by secs 
    """
    def func_wrapper():
        set_interval(callback, secs)
        callback()
    t = threading.Timer(secs, func_wrapper)
    t.start()
    return t


def set_timeout(callback: Callable[[Any], None], secs: float):
    threading.Timer(secs, callback)

import threading
from typing import Any, Callable


def set_interval(callback: Callable[[Any], None], secs: float):
    """
    Calls a callback function at specified intervals given by secs 
    """
    def func_wrapper():
        set_interval(callback, secs)
        callback()
    timed_thread = threading.Timer(secs, func_wrapper)
    timed_thread.start()
    return timed_thread


def set_timeout(callback: Callable[[Any], None], secs: float):
    """
    Calls a callback after wait a seconds amount
    """
    timed_thread = threading.Timer(secs, callback)
    timed_thread.start()

    return timed_thread

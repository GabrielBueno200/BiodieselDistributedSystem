from typing import Any, Callable
from threading import Event, Thread


def call_repeatedly(interval: float, func: Callable[[Any], None], *args: tuple) -> None:
    stopped = Event()

    def loop():
        while not stopped.wait(interval):  # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()
    return stopped.set

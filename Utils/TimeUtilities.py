import threading
from typing import Any, Callable
import time
from threading import Event, Thread

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()
    return stopped.set

#def set_interval(callback: Callable[[Any], None], secs: float):
#    """
#    Calls a callback function at specified intervals given by secs 
#    """
#    def func_wrapper():
#        set_interval(callback, secs)
#        callback()
#    timed_thread = threading.Timer(secs, func_wrapper)
#    timed_thread.start()
#    return timed_thread

#def count_time(callback, secs):
#    callback()
#    time.sleep(secs)
#    t = threading.Thread(target=count_time, args=(callback, secs, ))
#    t.daemon = True
#    t.start()
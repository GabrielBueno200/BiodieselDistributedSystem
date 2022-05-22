from threading import Event, Thread
import time

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval): # the first call is in `interval` secs
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

cancel_future_calls = call_repeatedly(10, print, "Hello, World")

print(type(cancel_future_calls))
for i in range(20):
    print(i)
    time.sleep(2)
    if i == 5:
        cancel_future_calls2 = call_repeatedly(2, print, "Bye, World")

cancel_future_calls() # stop future calls
cancel_future_calls2()
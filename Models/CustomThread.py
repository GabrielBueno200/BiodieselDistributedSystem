import threading

class CustomThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.daemon = True

    def join(self, timeout=None):
        if timeout is None:
            while self.is_alive():
                threading.Thread.join(self, 10)
        else:
            return threading.Thread.join(self, timeout)
import signal
import sys
from time import sleep

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
#signal.pause()#

for i in range(100):
    print(i)
    sleep(2)
import platform
import subprocess
from threading import Thread
import time
import sys
import os
import pathlib

def current_os():
    global python_name

    if platform.system() == 'Windows':
        python_name = 'python'
    elif platform.system() == 'Linux':
        python_name = f'python3'


if __name__ == "__main__":
    current_os()

    scripts = [
        f"{python_name} ./OilTankServer.py",
        f"{python_name} ./ReactorServer.py",
        f"{python_name} ./SodiumHydroxideTank.py",
        f"{python_name} ./EthanolTankServer.py",
        f"{python_name} ./DecanterServer.py",
        f"{python_name} ./GlycerinTankServer.py",
        f"{python_name} ./EthanolDryerServer.py",
        f"{python_name} ./BiodieselDryerServer.py",
        f"{python_name} ./FirstWashingServer.py",
        f"{python_name} ./SecondWashingServer.py",
        f"{python_name} ./ThirfWashingServer.py",
        f"{python_name} ./BiodieselTankServer.py"
    ]

    #all_threads = []
    all_scripts = " & ".join(scripts)
    #print(all_scripts)
    os.system(all_scripts)
    #    t = Thread(target=subprocess.run, args=(script.split(), ))
    #    all_threads.append(t)
    #    t.start()
#
    #[thread.join() for thread in all_threads]   
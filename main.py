import platform
import subprocess
import os
from threading import Thread

python_name = ""


def get_scripts():
    return [
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
        f"{python_name} ./ThirdWashingServer.py",
        f"{python_name} ./BiodieselTankServer.py"
    ]


def run_servers():
    global python_name

    if platform.system() == 'Windows':
        python_name = 'python'
        [Thread(target=subprocess.run, args=(script, )).start()
         for script in get_scripts()]

    elif platform.system() == 'Linux':
        python_name = f'python3'
        os.system(" & ".join(get_scripts()))


if __name__ == "__main__":
    run_servers()

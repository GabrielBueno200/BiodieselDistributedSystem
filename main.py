import subprocess
from threading import Thread
import time

scripts = [
    "python ./WashingServers.py",
    "python ./EthanolTankServer.py",
    "python ./SodiumHydroxideTank.py",
    "python ./GlycerinTankServer.py",
    "python ./BiodieselTankServer.py",
    "python ./ReactorServer.py",
    "python ./DecanterServer.py",
    "python ./OilTankServer.py",
    # "python ./DryersServers.py"
]

for script in scripts:
    t = Thread(target=subprocess.run, args=(script,))
    t.start()

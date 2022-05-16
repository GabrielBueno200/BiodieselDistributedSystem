import subprocess
from threading import Thread

scripts = [
    "python ./DecanterServer.py",
    "python ./ReactorServer.py",
    "python ./OilTankServer.py",
    "python ./EthanolTankServer.py",
    "python ./SodiumHydroxideTank.py",
    "python ./GlycerinTankServer.py",
    "python ./BiodieselTankServer.py",
    "python ./WashingServers.py",
    # "python ./DryersServers.py"
]

for script in scripts:
    t = Thread(target=subprocess.run, args=(script,))
    t.start()

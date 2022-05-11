from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class SodiumHydroxideServer(BaseComponentServer):
    print("Received sodium hydroxid from decanter")


SodiumHydroxideServer('localhost', ServersPorts.sodium_hydro_tank).run()

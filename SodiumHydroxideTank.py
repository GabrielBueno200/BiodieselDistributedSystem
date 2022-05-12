from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class SodiumHydroxideServer(BaseComponentServer):
    def process_substance(self, substance_payload: dict):
        print("Received sodium hydroxid from decanter")


SodiumHydroxideServer('localhost', ServersPorts.sodium_hydro_tank).run()

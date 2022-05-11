from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class BiodiselTankServer(BaseComponentServer):
    def process_substance(biodiesel_payload: dict):
        print("Received biodielsel from dryer")


BiodiselTankServer('localhost', ServersPorts.biodiesel_tank).run()

from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class BiodiselTankServer(BaseComponentServer):
    def process_substance(self, biodiesel_payload: dict):
        print("Received biodielsel from dryer")


BiodiselTankServer('localhost', ServersPorts.biodiesel_tank).run()

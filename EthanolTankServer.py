from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class EthanolTankServer(BaseComponentServer):
    def process_substance(self, ethanol_payload: dict):
        print("received ethanol from decanter")


EthanolTankServer('localhost', ServersPorts.ethanol_tank).run()

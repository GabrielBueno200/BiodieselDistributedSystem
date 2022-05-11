from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class EthanolTankServer(BaseComponentServer):
    def process_substance(self, ethanol_payload: dict):
        print("received ethanol from decanter")


EthanolTankServer('localhost', ServersPorts.ethanol_tank).run()

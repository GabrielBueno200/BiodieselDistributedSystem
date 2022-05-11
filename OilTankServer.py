from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class OilTankServer(BaseComponentServer):
    def process_substance(payload: dict):
        print(f"Received oil")


OilTankServer('localhost', ServersPorts.oil_tank).run()

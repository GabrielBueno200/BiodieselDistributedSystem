from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class EthanolDryerServer(BaseComponentServer):
    def process_substance(ethanol_payload: dict) -> None:
        print("drying ethanol")


class WashingsDryerServer(BaseComponentServer):
    def process_substance(washing_payload: dict) -> None:
        print("drying substance from washings")


EthanolDryerServer('localhost', ServersPorts.ethanol_tank_dryer).run()
WashingsDryerServer('localhost', ServersPorts.washings_dryer).run()

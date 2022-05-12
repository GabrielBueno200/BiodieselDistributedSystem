from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class WashingServer(BaseComponentServer):
    def process_substance(self, substance_payload: dict):
        print("washing substance...")


WashingServer('localhost', ServersPorts.first_washing).run()
WashingServer('localhost', ServersPorts.second_washing).run()
WashingServer('localhost', ServersPorts.third_washing).run()

from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class WashingServer(BaseComponentServer):
    def process_substance(self, substance_payload: dict):
        print("washing substance...")


first_washing = WashingServer('localhost', ServersPorts.first_washing)
second_washing = WashingServer('localhost', ServersPorts.second_washing)
third_washing = WashingServer('localhost', ServersPorts.third_washing)

first_washing.run()
second_washing.run()
third_washing.run()

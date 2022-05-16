from threading import Thread
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class WashingServer(BaseComponentServer):
    def process_substance(self, solution_payload: dict):
        self.log_info(f"received solution: {solution_payload}")
        print("washing substance...")


Thread(target=WashingServer('localhost', ServersPorts.first_washing).run).start()
Thread(target=WashingServer('localhost', ServersPorts.second_washing).run).start()
Thread(target=WashingServer('localhost', ServersPorts.third_washing).run).start()

from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Models.ComponentState import ComponentState


class BiodiselTankServer(BaseComponentServer):
    total_biodiesel = 0

    def process_substance(self, biodiesel_payload: dict):
        self.receive_biodiesel(biodiesel_payload["biodiesel_amount"])

        return ComponentState(self.total_biodiesel)

    def receive_biodiesel(self, biodiesel_amount: float):
        self.total_biodiesel += biodiesel_amount

        self.log_info(f"Received {biodiesel_amount}l of biodiesel")


BiodiselTankServer('localhost', ServersPorts.biodiesel_tank).run()

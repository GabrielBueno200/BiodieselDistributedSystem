from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Models.ComponentState import ComponentState


class GlycerinTankServer(BaseComponentServer):
    total_glycerin = 0

    def process_substance(self, glycerin_payload: dict):
        self.receive_gliceryn(glycerin_payload["glycerin_amount"])

        return ComponentState(self.total_glycerin)

    def receive_gliceryn(self, glycerin_amount: float):
        self.total_glycerin += glycerin_amount

        self.log_info(f"Received {glycerin_amount}l of glycerin")


GlycerinTankServer('localhost', ServersPorts.glycerin_tank).run()

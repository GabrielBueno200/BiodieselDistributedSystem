from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
import sys


class BiodiselTankServer(BaseComponentServer):
    def __init__(self, host, port) -> None:
        super().__init__(host, port)
        self.remaining_biodiesel = 0

    def signal_handler(self, sig, frame):
        sys.exit(0)

    def get_state(self):
        return {"occupied_capacity": self.remaining_biodiesel}

    def process_substance(self, biodiesel_payload: dict) -> None:
        biodiesel_amount = biodiesel_payload["solution_amount"]
        self.remaining_biodiesel += biodiesel_amount

        self.log_info(f"Received {biodiesel_amount}l of biodiesel")

        return self.get_state()


if __name__ == "__main__":
    BiodiselTankServer('localhost', ServersPorts.biodiesel_tank).run()

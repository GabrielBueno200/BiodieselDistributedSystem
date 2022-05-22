import sys
import json
import threading
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import call_repeatedly
from socket import AF_INET, SOCK_STREAM, socket
from BaseComponentServer import BaseComponentServer


class DecanterServer(BaseComponentServer):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.max_capacity = 10
        self.remaining_substances = 0
        self.cycles = 0
        self.is_resting = False
        self.max_limit_reached = False
        self.cancel_future_calls = call_repeatedly(
            interval=1, func=self.deplete_tank)

    def signal_handler(self, sig, frame):
        self.cancel_future_calls()
        sys.exit(0)

    def get_state(self):
        return {
            "occupied_capacity": self.remaining_substances,
            "is_resting": self.is_resting,
            "cycles": self.cycles,
            "max_limit_reached": self.max_limit_reached,
        }

    def process_substance(self, substances_payload: dict):
        if not self.is_resting and not self.max_limit_reached:
            substances_amount = substances_payload["substances_amount"]
            self.remaining_substances += substances_amount

            self.is_resting = True
            self.cycles += 1

            time_to_rest = 5
            threading.Timer(time_to_rest, self.stop_resting).start()

            self.log_info(
                f"Received {substances_amount}l of sodium, ethanol and oil from reactor")

        if self.remaining_substances == self.max_capacity:
            self.max_limit_reached = True

        return self.get_state()

    def stop_resting(self):
        self.is_resting = False

    def deplete_tank(self):
        if not self.is_resting and self.remaining_substances > 0:
            glycerin_amount = self.remaining_substances * 0.01
            ethanol_amount = self.remaining_substances * 0.03
            solution_amount = self.remaining_substances * 0.96

            self.transfer_substance(SubstanceType.GLYCERIN,
                                    glycerin_amount, ServersPorts.glycerin_tank)

            self.transfer_substance(SubstanceType.ETHANOL,
                                    ethanol_amount, ServersPorts.ethanol_tank_dryer)

            self.transfer_substance(SubstanceType.SOLUTION,
                                    solution_amount, ServersPorts.first_washing)

    def transfer_substance(self, substance: SubstanceType, substance_amount: float, server_port: ServersPorts):
        with socket(AF_INET, SOCK_STREAM) as component_sock:
            component_sock.connect(("localhost", server_port))

            component_sock.sendall(json.dumps(
                {f"{substance}_amount": substance_amount}).encode())

            self.remaining_substances -= substance_amount

            component_sock.recv(self.data_payload)


if __name__ == "__main__":
    DecanterServer('localhost', ServersPorts.decanter).run()

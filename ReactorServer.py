import sys
import json
from time import sleep
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from BaseComponentServer import BaseComponentServer
from socket import socket, AF_INET, SOCK_STREAM


class ReactorServer(BaseComponentServer):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

        self.max_capacity = 5

        self.max_sodium = self.max_capacity / 4
        self.max_ethanol = self.max_capacity / 4
        self.max_oil = self.max_capacity / 2

        self.substances_amount = {
            SubstanceType.OIL: 0,
            SubstanceType.SODIUM: 0,
            SubstanceType.ETHANOL: 0
        }

        self.remaining_substances = 0
        self.substances_outflow = 1

        self.cycles = 0

        self.is_processing = False

    def signal_handler(self, sig, frame):
        sys.exit(0)

    def get_state(self):
        return {
            "occupied_capacity": self.remaining_substances,
            "is_busy": self.is_processing,
            "cycles": self.cycles,
            **self.substances_amount
        }

    def process_substance(self, substance_payload: dict):
        if self.is_processing or self.check_can_process():
            return {"is_busy": True}

        substance_type = substance_payload["substance_type"]
        substance_amount = substance_payload["substance_amount"]

        self.remaining_substances = sum(self.substances_amount.values())

        self.log_info(f"received {substance_amount}l of {substance_type}")

        return self.transfer_substance(substance_type, substance_amount)

    def check_can_process(self):
        max_substances_reached = self.max_sodium_reached(
        ) and self.max_ethanol_reached() and self.max_oil_reached()

        decanter_state = self.check_component_state(ServersPorts.decanter)
        decanter_available = not decanter_state["max_limit_reached"] and not decanter_state["is_resting"]

        if decanter_available and max_substances_reached and not self.is_processing:
            self.is_processing = True
            self.cycles += 1
            self.transfer_substances_to_decanter()
            return True

        return False

    def transfer_substances_to_decanter(self):
        while self.remaining_substances > 0:
            substances_to_transfer = 0

            if self.remaining_substances >= self.substances_outflow:
                substances_to_transfer = self.substances_outflow
            else:
                substances_to_transfer = self.remaining_substances

            with socket(AF_INET, SOCK_STREAM) as decanter_sock:
                decanter_sock.connect(("localhost", ServersPorts.decanter))

                decanter_sock.sendall(json.dumps(
                    {"substances_amount": substances_to_transfer}).encode())

                decanter_sock.recv(1024)

            self.remaining_substances -= substances_to_transfer
            sleep(1)

        self.substances_amount[SubstanceType.OIL] = 0
        self.substances_amount[SubstanceType.ETHANOL] = 0
        self.substances_amount[SubstanceType.SODIUM] = 0

        self.is_processing = False

    def max_oil_reached(self):
        return self.substances_amount[SubstanceType.OIL] == self.max_oil

    def max_sodium_reached(self):
        return self.substances_amount[SubstanceType.SODIUM] == self.max_sodium

    def max_ethanol_reached(self):
        return self.substances_amount[SubstanceType.ETHANOL] == self.max_ethanol

    def transfer_substance(self, substance_type: SubstanceType, transfer_amount: float) -> dict:
        max_substance_amount = 0
        current_substance_amount = self.substances_amount[substance_type]

        if substance_type == SubstanceType.OIL:
            max_substance_amount = self.max_oil
        elif substance_type == SubstanceType.ETHANOL:
            max_substance_amount = self.max_ethanol
        elif substance_type == SubstanceType.SODIUM:
            max_substance_amount = self.max_sodium

        total_after_transference = current_substance_amount + \
            transfer_amount

        if total_after_transference > max_substance_amount:
            transfer_amount = max_substance_amount - current_substance_amount

        self.substances_amount[substance_type] += transfer_amount
        return {"total_transfered": transfer_amount, "is_busy": False}


if __name__ == "__main__":
    ReactorServer('localhost', ServersPorts.reactor).run()

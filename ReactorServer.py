import sys
import json
from time import sleep
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from socket import socket, AF_INET, SOCK_STREAM
from BaseComponentServer import BaseComponentServer


class ReactorServer(BaseComponentServer):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)

        self.is_processing = False
        self.max_capacity = 5

        self.substances_amount = {
            SubstanceType.OIL: 0,
            SubstanceType.SODIUM: 0,
            SubstanceType.ETHANOL: 0
        }

        self.max_substance_amount = {
            SubstanceType.OIL: self.max_capacity / 2,
            SubstanceType.SODIUM: self.max_capacity / 4,
            SubstanceType.ETHANOL: self.max_capacity / 4
        }

        self.remaining_substances = 0
        self.substances_outflow = 1

        self.cycles = 0

    def signal_handler(self, sig, frame):
        sys.exit(0)

    def get_state(self):
        return {
            "occupied_capacity": self.remaining_substances,
            "is_processing": self.is_processing,
            "cycles": self.cycles,
            **self.substances_amount
        }

    def process_substance(self, substance_payload: dict):
        if self.is_processing or self.check_can_process():
            return {"is_processing": True}

        substance_type = substance_payload["substance_type"]
        substance_amount = substance_payload["substance_amount"]

        self.remaining_substances = sum(self.substances_amount.values())

        self.log_info(f"received {substance_amount}l of {substance_type}")

        return self.transfer_substance(substance_type, substance_amount)

    def check_can_process(self):
        max_oil_reached = self.substances_amount[
            SubstanceType.OIL] == self.max_substance_amount[SubstanceType.OIL]
        max_sodium_reached = self.substances_amount[
            SubstanceType.SODIUM] == self.max_substance_amount[SubstanceType.SODIUM]
        max_ethanol_reached = self.substances_amount[
            SubstanceType.ETHANOL] == self.max_substance_amount[SubstanceType.ETHANOL]

        max_substances_reached = max_oil_reached and max_sodium_reached and max_ethanol_reached

        if max_substances_reached and not self.is_processing:
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

    def transfer_substance(self, substance_type: SubstanceType, transfer_amount: float) -> dict:
        max_substance_amount = self.max_substance_amount[substance_type]
        current_substance_amount = self.substances_amount[substance_type]

        total_after_transference = current_substance_amount + transfer_amount

        if total_after_transference > max_substance_amount:
            transfer_amount = max_substance_amount - current_substance_amount

        self.substances_amount[substance_type] += transfer_amount

        return {"total_transfered": transfer_amount, "is_processing": False}


if __name__ == "__main__":
    ReactorServer('localhost', ServersPorts.reactor).run()

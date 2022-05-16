import json
from socket import AF_INET, SOCK_STREAM, socket
from threading import Timer
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import set_timeout


class ReactorServer(BaseComponentServer):
    max_capacity = 5

    substances_amount = {
        SubstanceType.OIL: 0,
        SubstanceType.SODIUM: 0,
        SubstanceType.ETHANOL: 0
    }

    remaining_substances = 0
    substances_outflow = 5

    processing_thread_running = None

    def process_substance(self, substance_payload: dict):
        if self.check_is_processing():
            if not self.processing_thread_running:
                self.processing_thread_running = set_timeout(
                    self.transfer_substances_to_decanter, 1)

            return {"occupied_capacity": self.remaining_substances, "is_busy": True, "max_substance_reached": False}

        substance_type = substance_payload["substance_type"]
        substance_amount = substance_payload["substance_amount"]

        self.remaining_substances = sum(self.substances_amount.values())

        if not self.check_can_transfer_substance(substance_type):
            return {"occupied_capacity": self.remaining_substances, "is_busy": False, "max_substance_reached": True}

        self.substances_amount[substance_type] += substance_amount
        self.remaining_substances += substance_amount
        self.log_info(f"received {substance_amount}l of {substance_type}")

        return {"occupied_capacity": self.remaining_substances, "is_busy": False, "max_substance_reached": False}

    def check_is_processing(self):
        return self.max_sodium_amount() and self.max_ethanol_amount() and self.max_oil_amount()

    def max_oil_amount(
        self): return self.substances_amount[SubstanceType.OIL] >= self.max_capacity / 2

    def max_sodium_amount(
        self): return self.substances_amount[SubstanceType.SODIUM] >= self.max_capacity / 4

    def max_ethanol_amount(
        self): return self.substances_amount[SubstanceType.ETHANOL] >= self.max_capacity / 4

    def check_can_transfer_substance(self, substance_type) -> bool:
        if substance_type == SubstanceType.OIL:
            return not self.max_oil_amount()
        elif substance_type == SubstanceType.ETHANOL:
            return not self.max_ethanol_amount()
        elif substance_type == SubstanceType.SODIUM:
            return not self.max_sodium_amount()

    def transfer_substances_to_decanter(self):
        while self.remaining_substances > 0:
            substances_to_transfer = 0

            if (self.remaining_substances - self.substances_outflow > 0):
                substances_to_transfer = self.substances_outflow
            else:
                substances_to_transfer = self.remaining_substances

            self.log_info("entrou")

            with socket(AF_INET, SOCK_STREAM) as decanter_sock:
                decanter_sock.connect(("localhost", ServersPorts.decanter))

                decanter_sock.sendall(json.dumps(
                    {"substances_amount": substances_to_transfer}).encode())

                decanter_response = decanter_sock.recv(1024)

                if decanter_response:
                    decanter_state = json.loads(decanter_response.decode())

                    if not decanter_state["is_busy"]:
                        self.log_info(
                            f"transfering to decanter: {substances_to_transfer}l")
                        self.remaining_substances -= substances_to_transfer

        self.substances_amount[SubstanceType.OIL] = 0
        self.substances_amount[SubstanceType.GLYCERIN] = 0
        self.substances_amount[SubstanceType.SODIUM] = 0

        self.processing_thread_running = None

if __name__ == "__main__":
    ReactorServer('localhost', ServersPorts.reactor).run()

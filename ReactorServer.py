import json
from socket import AF_INET, SOCK_STREAM, socket
from threading import Timer
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Models.ComponentState import ComponentState
from Utils.TimeUtilities import set_timeout


class ReactorServer(BaseComponentServer):
    max_capacity = 5

    substances_amount = {
        SubstanceType.OIL: 0,
        SubstanceType.SODIUM: 0,
        SubstanceType.ETHANOL: 0
    }

    remaining_substances = 0
    substances_outflow = 1
    is_processing = False
    processing_thread: Timer = None

    def process_substance(self, substance_payload: dict):
        substance_type = substance_payload["substance_type"]
        substance_amount = substance_payload["substance_amount"]

        self.remaining_substances = sum(self.substances_amount.values())
        self.is_processing = self.check_processing_start()

        if not self.is_processing:
            self.substances_amount[substance_type] += substance_amount
            self.remaining_substances += self.substances_amount[substance_type]

            self.log_info(f"received {substance_amount}l of {substance_type}")
            return ComponentState(self.remaining_substances)
        else:
            return ComponentState(occupied_capacity=self.remaining_substances, is_busy=True)

    def check_processing_start(self):
        has_max_oil = self.substances_amount[SubstanceType.OIL] >= self.max_capacity / 2
        has_max_sodium = self.substances_amount[SubstanceType.SODIUM] >= self.max_capacity / 4
        has_max_ethanol = self.substances_amount[SubstanceType.ETHANOL] >= self.max_capacity / 4

        can_process = has_max_oil and has_max_ethanol and has_max_sodium

        if not self.is_processing and can_process:
            self.processing_thread = set_timeout(
                self.transfer_substances_to_decanter, secs=1)

        return can_process

    def transfer_substances_to_decanter(self):
        if self.remaining_substances > 0:
            substances_to_transfer = 0

            if (self.remaining_substances - self.substances_outflow > 0):
                substances_to_transfer = self.substances_outflow
            else:
                substances_to_transfer = self.remaining_substances

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


ReactorServer('localhost', ServersPorts.reactor).run()

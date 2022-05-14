from socket import AF_INET, SOCK_STREAM, socket
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

    def process_substance(self, substance_payload: dict):
        substance_type = substance_payload["substance_type"]
        substance_amount = substance_payload["substance_amount"]

        occupied_capacity = sum(self.substances_amount.values())
        is_busy = self.check_processing_start()

        if not is_busy:
            self.substances_amount[substance_type] += substance_amount
            occupied_capacity += self.substances_amount[substance_type]

            self.log_info(f"received {substance_amount}l of {substance_type}")
            return ComponentState(occupied_capacity)
        else:
            set_timeout(self.start_processing, secs=1)
            return ComponentState(occupied_capacity=0, is_busy=is_busy)

    def start_processing(self):
        self.substances_amount = {x: 0 for x in self.substances_amount}

        with socket(AF_INET, SOCK_STREAM) as decanter_sock:
            decanter_sock.sendall(str({"processed_substance_amount": 5}))

    def check_processing_start(self):
        has_max_oil = self.substances_amount[SubstanceType.OIL] >= self.max_capacity / 2
        has_max_sodium = self.substances_amount[SubstanceType.SODIUM] >= self.max_capacity / 4
        has_max_ethanol = self.substances_amount[SubstanceType.ETHANOL] >= self.max_capacity / 4

        return has_max_oil and has_max_ethanol and has_max_sodium


ReactorServer('localhost', ServersPorts.reactor).run()

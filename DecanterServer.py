import json
from socket import AF_INET, SOCK_STREAM, socket
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Models.ComponentState import ComponentState
from Utils.TimeUtilities import set_timeout


class DecanterServer(BaseComponentServer):
    max_capacity: int = 10
    remaining_substances = 0
    is_resting = False

    def process_substance(self, substances_payload: dict):
        substances_amount = substances_payload["substances_amount"]

        if not self.is_resting:
            self.remaining_substances += substances_amount
            self.is_resting = True
            set_timeout(self.start_resting, secs=5)

            self.log_info(
                f"Received {substances_amount}l of sodium, ethanol and oil from reactor")
            return ComponentState(self.remaining_substances)
        else:
            return ComponentState(self.remaining_substances, is_busy=True)

    def start_resting(self):
        glycerin_amount = self.remaining_substances * 0.01
        ethanol_amount = self.remaining_substances * 0.03
        solution_amount = self.remaining_substances * 0.96

        self.transfer_substance(SubstanceType.GLYCERIN,
                                glycerin_amount, ServersPorts.glycerin_tank)

        self.transfer_substance(SubstanceType.ETHANOL,
                                ethanol_amount, ServersPorts.ethanol_tank)

        self.transfer_substance(SubstanceType.SOLUTION,
                                solution_amount, ServersPorts.first_washing)

        self.is_resting = False

    def transfer_substance(self, substance: SubstanceType, substance_amount: float, server_port: ServersPorts):
        with socket(AF_INET, SOCK_STREAM) as component_sock:
            component_sock.connect(("localhost", server_port))

            component_sock.sendall(json.dumps(
                {f"{substance}_amount": substance_amount}).encode())

            component_sock.recv(1024)


DecanterServer('localhost', ServersPorts.decanter).run()

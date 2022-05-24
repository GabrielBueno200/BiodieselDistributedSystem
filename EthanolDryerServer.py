from socket import AF_INET, SOCK_STREAM, socket
import sys
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import call_repeatedly
import json


class EthanolDryerServer(BaseComponentServer):
    def __init__(self, host, port) -> None:
        super().__init__(host, port)
        self.substances_outflow = 1
        self.loss = 0.005
        self.remaining_ethanol = 0
        self.cancel_future_calls = call_repeatedly(
            interval=5, func=self.transfer_to_ethanol_tank)

    def signal_handler(self, sig, frame):
        self.cancel_future_calls()
        sys.exit(0)

    def get_state(self):
        return {"occupied_capacity": self.remaining_ethanol}

    def process_substance(self, ethanol_payload: dict) -> None:
        ethanol_amount = ethanol_payload["ethanol_amount"]
        self.remaining_ethanol += ethanol_amount

    def transfer_to_ethanol_tank(self):
        if self.remaining_ethanol > 0:

            substances_to_transfer = 0

            if self.remaining_ethanol >= self.substances_outflow:
                substances_to_transfer = self.substances_outflow
            else:
                substances_to_transfer = self.remaining_ethanol

            ethanol_to_send = substances_to_transfer*(1-self.loss)

            with socket(AF_INET, SOCK_STREAM) as component_sock:
                component_sock.connect(
                    ("localhost", ServersPorts.ethanol_tank))

                component_sock.sendall(json.dumps(
                    {f"{SubstanceType.ETHANOL}_amount": ethanol_to_send}).encode())

                self.remaining_ethanol -= substances_to_transfer

                component_sock.recv(1024)


if __name__ == "__main__":
    EthanolDryerServer('localhost', ServersPorts.ethanol_tank_dryer).run()

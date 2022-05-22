from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from socket import socket, AF_INET, SOCK_STREAM
import json
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import call_repeatedly
import sys


class EthanolTankServer(BaseComponentServer):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.remaining_ethanol = 0
        self.ethanol_outflow = 1
        self.cancel_future_calls = call_repeatedly(
            interval=1, func=self.transfer_ethanol_to_reactor)

    def signal_handler(self, sig, frame):
        self.cancel_future_calls()
        sys.exit(0)

    def get_state(self):
        return {"occupied_capacity": self.remaining_ethanol}

    def process_substance(self, ethanol_payload: dict) -> dict or None:
        ethanol_amount = ethanol_payload["ethanol_amount"]
        self.remaining_ethanol += ethanol_amount

        self.log_info(f"Received {ethanol_amount}l of ethanol")

        return self.get_state()

    def transfer_ethanol_to_reactor(self):
        if self.remaining_ethanol > 0:
            ethanol_to_transfer = 0

            if self.remaining_ethanol >= self.ethanol_outflow:
                ethanol_to_transfer = self.ethanol_outflow
            else:
                ethanol_to_transfer = self.remaining_ethanol

            with socket(AF_INET, SOCK_STREAM) as reactor_sock:
                reactor_sock.connect(("localhost", ServersPorts.reactor))

                payload_to_reactor = {
                    "substance_type": SubstanceType.ETHANOL,
                    "substance_amount": ethanol_to_transfer
                }

                reactor_sock.sendall(json.dumps(payload_to_reactor).encode())

                reactor_response = reactor_sock.recv(self.data_payload)

                if reactor_response:
                    reactor_state = json.loads(reactor_response.decode())

                    if not reactor_state["is_busy"] and not reactor_state["max_substance_reached"]:
                        self.log_info(
                            f"transfering to reactor: {ethanol_to_transfer}l")
                        self.remaining_ethanol -= ethanol_to_transfer

    @staticmethod
    def receive_ethanol(ethanol_tank_client_socket: socket):
        ethanol_to_deposit = 0.25

        payload = json.dumps({
            "ethanol_amount": ethanol_to_deposit
        })

        ethanol_tank_client_socket.sendall(payload.encode())


if __name__ == "__main__":
    EthanolTankServer('localhost', ServersPorts.ethanol_tank).run()

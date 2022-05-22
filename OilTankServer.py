from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from socket import socket, AF_INET, SOCK_STREAM
from random import uniform
import json
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import call_repeatedly
import sys


class OilTankServer(BaseComponentServer):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.remaining_oil = 0
        self.oil_outflow = 0.75
        self.cancel_future_calls = call_repeatedly(
            interval=1, func=self.transfer_oil_to_reactor)

    def signal_handler(self, sig, frame):
        self.cancel_future_calls()
        sys.exit(0)

    def get_state(self):
        return {"occupied_capacity": self.remaining_oil}

    def process_substance(self, oil_payload: dict):
        oil_amount = oil_payload["oil_amount"]

        self.remaining_oil += oil_amount

        self.log_info(f"Received {oil_amount}l of oil")

        return self.get_state()

    @staticmethod
    def receive_oil(oil_tank_client_socket: socket):
        oil_to_deposit = uniform(1, 2)

        payload = json.dumps({
            "oil_amount": oil_to_deposit
        })

        oil_tank_client_socket.sendall(payload.encode())

    def transfer_oil_to_reactor(self):
        if self.remaining_oil > 0:
            oil_to_transfer = 0

            if self.remaining_oil >= self.oil_outflow:  # More than 0.75
                oil_to_transfer = self.oil_outflow
            else:
                oil_to_transfer = self.remaining_oil

            with socket(AF_INET, SOCK_STREAM) as reactor_sock:
                reactor_sock.connect(("localhost", ServersPorts.reactor))

                payload_to_reactor = {
                    "substance_type": SubstanceType.OIL,
                    "substance_amount": oil_to_transfer
                }

                reactor_sock.sendall(json.dumps(payload_to_reactor).encode())

                reactor_response = reactor_sock.recv(self.data_payload)

                if reactor_response:

                    reactor_state = json.loads(reactor_response.decode())

                    if not reactor_state["is_busy"]:
                        self.log_info(
                            f"transfering to reactor: {oil_to_transfer}l")
                        self.log_info(reactor_state["total_transfered"])
                        self.remaining_oil -= reactor_state["total_transfered"]


if __name__ == "__main__":
    OilTankServer('localhost', ServersPorts.oil_tank).run()

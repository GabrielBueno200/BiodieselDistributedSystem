import json
from random import uniform
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Models.ComponentState import ComponentState
from Utils.TimeUtilities import set_interval
from socket import socket, AF_INET, SOCK_STREAM
from BaseComponentServer import BaseComponentServer


class OilTankServer(BaseComponentServer):
    remaining_oil: int = 0
    oil_outflow: float = 0.75

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.start_async_routines()

    def start_async_routines(self):
        time_transfer_oil_reactor = 1
        set_interval(self.transfer_oil_to_reactor, time_transfer_oil_reactor)

    def process_substance(self, oil_payload: dict):
        oil_amount = oil_payload["oil_amount"]
        self.remaining_oil += oil_amount

        self.log_info(
            f"Received {oil_amount}l of oil")

        return ComponentState(self.remaining_oil)

    def transfer_oil_to_reactor(self):
        if self.remaining_oil > 0:
            oil_to_transfer = 0

            if (self.remaining_oil - self.oil_outflow > 0):
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

                reactor_response = reactor_sock.recv(1024)

                if reactor_response:
                    reactor_state = json.loads(reactor_response.decode())

                    if not reactor_state["is_busy"]:
                        self.log_info(
                            f"transfering to reactor: {oil_to_transfer}l")
                        self.remaining_oil -= oil_to_transfer

    @staticmethod
    def receive_oil(oil_tank_client_socket: socket):
        oil_to_deposit = uniform(1, 2)
        oil_tank_client_socket.sendall(json.dumps({
            "oil_amount": oil_to_deposit
        }).encode())


if __name__ == "__main__":
    OilTankServer('localhost', ServersPorts.oil_tank).run()

from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from socket import socket, AF_INET, SOCK_STREAM
import json
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import call_repeatedly
import sys


class SodiumHydroxideServer(BaseComponentServer):
    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.remaining_sodium = 0
        self.sodium_outflow = 1
        self.cancel_future_calls = call_repeatedly(
            interval=1, func=self.transfer_sodium_to_reactor)

    def signal_handler(self, sig, frame):
        self.cancel_future_calls()
        sys.exit(0)

    def get_state(self):
        return {"occupied_capacity": self.remaining_sodium}

    def process_substance(self, sodium_payload: dict):
        sodium_amount = sodium_payload["sodium_amount"]
        self.remaining_sodium += sodium_amount

        self.log_info(f"Received {sodium_amount}l of hydroxide sodium")

        return self.get_state()

    def transfer_sodium_to_reactor(self):
        if self.remaining_sodium > 0:
            sodium_to_transfer = 0

            if self.remaining_sodium >= self.sodium_outflow:
                sodium_to_transfer = self.sodium_outflow
            else:
                sodium_to_transfer = self.remaining_sodium

            with socket(AF_INET, SOCK_STREAM) as reactor_sock:
                reactor_sock.connect(("localhost", ServersPorts.reactor))

                payload_to_reactor = {
                    "substance_type": SubstanceType.SODIUM,
                    "substance_amount": sodium_to_transfer
                }

                reactor_sock.sendall(json.dumps(payload_to_reactor).encode())

                reactor_response = reactor_sock.recv(self.data_payload)

                if reactor_response:
                    reactor_state = json.loads(reactor_response.decode())

                    if not reactor_state["is_busy"] and not reactor_state["max_substance_reached"]:
                        # self.log_info(
                        #     f"transfering to reactor: {sodium_to_transfer}l")
                        self.remaining_sodium -= sodium_to_transfer

    @staticmethod
    def receive_sodium(sodium_tank_client_socket: socket):
        sodium_to_deposit = 0.5

        content = json.dumps({
            "sodium_amount": sodium_to_deposit
        })

        sodium_tank_client_socket.sendall(content.encode())


if __name__ == "__main__":
    SodiumHydroxideServer('localhost', ServersPorts.sodium_hydro_tank).run()

import json
from socket import AF_INET, SOCK_STREAM, socket
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import set_interval


class SodiumHydroxideServer(BaseComponentServer):
    remaining_sodium: float = 0
    sodium_outflow: float = 1

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.start_async_routines()

    def start_async_routines(self):
        time_transfer_sodium_reactor = 1
        set_interval(self.transfer_sodium_to_reactor,
                     time_transfer_sodium_reactor)

    def process_substance(self, sodium_payload: dict):
        sodium_amount = sodium_payload["sodium_amount"]
        self.remaining_sodium += sodium_amount

        # self.log_info(f"Received {sodium_amount}l of hydroxide sodium")

        return self.get_state()

    def get_state(self):
        return {"occupied_capacity": self.remaining_sodium}

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

                reactor_response = reactor_sock.recv(1024)

                if reactor_response:
                    reactor_state = json.loads(reactor_response.decode())

                    if not reactor_state["is_busy"] and not reactor_state["max_substance_reached"]:
                        # self.log_info(
                        #     f"transfering to reactor: {sodium_to_transfer}l")
                        self.remaining_sodium -= sodium_to_transfer

    @staticmethod
    def receive_sodium(sodium_tank_client_socket: socket):
        sodium_to_deposit = 0.5
        sodium_tank_client_socket.sendall(json.dumps({
            "sodium_amount": sodium_to_deposit
        }).encode())


if __name__ == "__main__":
    SodiumHydroxideServer('localhost', ServersPorts.sodium_hydro_tank).run()

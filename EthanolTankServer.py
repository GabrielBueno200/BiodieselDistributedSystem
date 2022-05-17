import json
from socket import AF_INET, SOCK_STREAM, socket
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from Utils.TimeUtilities import set_interval


class EthanolTankServer(BaseComponentServer):
    remaining_ethanol: float = 0
    ethanol_outflow: float = 1

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.start_async_routines()

    def start_async_routines(self):
        time_transfer_ethanol_reactor = 1
        set_interval(self.transfer_ethanol_to_reactor,
                     time_transfer_ethanol_reactor)

    def process_substance(self, ethanol_payload: dict) -> dict or None:
        ethanol_amount = ethanol_payload["ethanol_amount"]
        self.remaining_ethanol += ethanol_amount

        # self.log_info(f"Received {ethanol_amount}l of ethanol")

        return self.get_state()

    def get_state(self):
        return {"occupied_capacity": self.remaining_ethanol}

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

                reactor_response = reactor_sock.recv(1024)

                if reactor_response:
                    reactor_state = json.loads(reactor_response.decode())

                    if not reactor_state["is_busy"] and not reactor_state["max_substance_reached"]:
                        # self.log_info(
                        #     f"transfering to reactor: {ethanol_to_transfer}l")
                        self.remaining_ethanol -= ethanol_to_transfer

    @staticmethod
    def receive_ethanol(ethanol_tank_client_socket: socket):
        ethanol_to_deposit = 0.25
        ethanol_tank_client_socket.sendall(json.dumps({
            "ethanol_amount": ethanol_to_deposit
        }).encode())


if __name__ == "__main__":
    EthanolTankServer('localhost', ServersPorts.ethanol_tank).run()

import json
from socket import socket
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Models.ComponentState import ComponentState


class EthanolTankServer(BaseComponentServer):
    total_ethanol = 0

    def process_substance(self, ethanol_payload: dict) -> ComponentState or None:
        ethanol_amount = ethanol_payload["ethanol_amount"]
        self.total_ethanol += ethanol_amount

        print(f"Received {ethanol_amount}l of ethanol")

        return ComponentState(self.total_ethanol)

    @staticmethod
    def receive_ethanol(ethanol_tank_client_socket: socket):
        ethanol_to_deposit = 0.25
        ethanol_tank_client_socket.sendall(json.dumps({
            "ethanol_amount": ethanol_to_deposit
        }).encode())


if __name__ == "__main__":
    EthanolTankServer('localhost', ServersPorts.ethanol_tank).run()

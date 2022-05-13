import json
from socket import socket
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class EthanolTankServer(BaseComponentServer):
    def process_substance(self, ethanol_payload: dict):
        ethanol_amount = ethanol_payload["ethanol_amount"]

        print(f"Received {ethanol_amount}l of ethanol")

    @staticmethod
    def receive_ethanol(ethanol_tank_client_socket: socket):
        ethanol_to_deposit = 0.25
        ethanol_tank_client_socket.sendall(json.dumps({
            "ethanol_amount": ethanol_to_deposit
        }).encode())


if __name__ == "__main__":
    EthanolTankServer('localhost', ServersPorts.ethanol_tank).run()

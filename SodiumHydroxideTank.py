import json
from socket import socket
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class SodiumHydroxideServer(BaseComponentServer):
    def process_substance(self, sodium_payload: dict):
        sodium_amount = sodium_payload["sodium_amount"]

        print(f"Received {sodium_amount}l of hydroxide sodium")

    @staticmethod
    def receive_sodium(sodium_tank_client_socket: socket):
        sodium_to_deposit = 0.25
        sodium_tank_client_socket.sendall(json.dumps({
            "sodium_amount": sodium_to_deposit
        }).encode())


if __name__ == "__main__":
    SodiumHydroxideServer('localhost', ServersPorts.sodium_hydro_tank).run()

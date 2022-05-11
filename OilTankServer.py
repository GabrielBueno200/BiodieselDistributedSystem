from socket import socket, AF_INET, SOCK_STREAM
from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class OilTankServer(BaseComponentServer):
    def process_substance(self, oil_payload: dict):
        print(f"Received oil")

        with socket(AF_INET, SOCK_STREAM) as reactor_sock:
            reactor_sock.connect(("localhost", ServersPorts.reactor))

            reactor_sock.sendall(str({"message": "Enviando óleo"}).encode())


OilTankServer('localhost', ServersPorts.oil_tank).run()

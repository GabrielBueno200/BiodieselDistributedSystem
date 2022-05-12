from socket import socket, AF_INET, SOCK_STREAM
import json
from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts
from Enums.Substance import Substance


class OilTankServer(BaseComponentServer):
    total_oil = 0

    def process_substance(self, oil_payload: dict):
        oil_amount = oil_payload["oil_amount"]
        self.total_oil += oil_amount

        print(
            f"Received {oil_amount}l of oil | Total in tank: {self.total_oil}")

        with socket(AF_INET, SOCK_STREAM) as reactor_sock:
            reactor_sock.connect(("localhost", ServersPorts.reactor))

            payload_to_reactor = {
                "substance_type": Substance.OIL,
                "substance_amount": oil_amount
            }

            reactor_sock.sendall(json.dumps(payload_to_reactor).encode())


OilTankServer('localhost', ServersPorts.oil_tank).run()

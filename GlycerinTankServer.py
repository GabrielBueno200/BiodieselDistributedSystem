from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer


class GlycerinTankServer(BaseComponentServer):
    def process_substance(glycerin_payload: dict):
        print(f"Received glycerin from decanter")


GlycerinTankServer('localhost', 8086).run()

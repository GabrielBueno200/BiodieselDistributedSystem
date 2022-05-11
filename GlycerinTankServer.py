from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class GlycerinTankServer(BaseComponentServer):
    def process_substance(self, glycerin_payload: dict):
        print(f"Received glycerin from decanter")


GlycerinTankServer('localhost', ServersPorts.glycerin_tank).run()

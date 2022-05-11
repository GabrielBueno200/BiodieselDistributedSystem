from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class ReactorServer(BaseComponentServer):
    def process_substance(self, oil_payload: dict):
        print(f"received oil : {oil_payload}")


ReactorServer('localhost', ServersPorts.reactor).run()

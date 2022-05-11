from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer
from Mapping.Ports import ServersPorts


class ReactorServer(BaseComponentServer):
    def process_substance(oil_payload: dict):
        print("received oil")


ReactorServer('localhost', ServersPorts.reactor)

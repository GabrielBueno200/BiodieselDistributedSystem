from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer


class ReactorServer(BaseComponentServer):
    def process_substance(oil_payload: dict):
        print("received oil")


ReactorServer('localhost', 8080)

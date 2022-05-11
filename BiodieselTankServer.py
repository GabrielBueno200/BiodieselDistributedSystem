from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer


class BiodiselTankServer(BaseComponentServer):
    def process_substance(biodiesel_payload: dict):
        print("Received biodielsel from dryer")


BiodiselTankServer('localhost', 8084).run()

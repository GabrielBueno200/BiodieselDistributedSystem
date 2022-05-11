from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer


class WashingServer(BaseComponentServer):
    def process_substance(substance_payload: dict):
        print("washing substance...")


first_washing = WashingServer('localhost', 8089)
second_washing = WashingServer('localhost', 8090)
third_washing = WashingServer('localhost', 8091)

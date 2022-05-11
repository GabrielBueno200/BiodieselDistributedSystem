from abc import abstractmethod
from socket import socket, AF_INET, SOCK_STREAM

from BaseComponentServer import BaseComponentServer


class EthanolDryerServer(BaseComponentServer):
    def process_substance(ethanol_payload: dict) -> None:
        print("drying ethanol")


class WashingsDryerServer(BaseComponentServer):
    def process_substance(washing_payload: dict) -> None:
        print("drying substance from washings")


EthanolDryerServer('localhost', 8087).run()
WashingsDryerServer('localhost', 8088).run()

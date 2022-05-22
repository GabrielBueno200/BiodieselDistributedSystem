from abc import ABC, abstractmethod
from socket import socket, AF_INET, SOCK_STREAM
import json
from _thread import *
import signal

from Enums.Ports import ServersPorts


class BaseComponentServer(ABC):
    def __init__(self, host, port) -> None:
        self.host = host
        self.port = port
        self.data_payload = 1024
        signal.signal(signal.SIGINT, self.signal_handler)

    @abstractmethod
    def signal_handler(self, sig, frame):
        pass

    @abstractmethod
    def get_state(self): pass

    @abstractmethod
    def process_substance(self, payload: dict) -> None: pass

    def log_info(self, info: str):
        print(f"{self.__class__.__name__}: {info}")

    def check_component_state(self, port: ServersPorts):
        with socket(AF_INET, SOCK_STREAM) as component_sock:
            component_sock.connect(("localhost", port))
            component_sock.sendall("get_state".encode())

            component_response = component_sock.recv(self.data_payload)

            component_state = json.loads(component_response.decode())

            return component_state

    def handle_data(self, client_connection: socket):
        while True:
            data = client_connection.recv(self.data_payload)

            if data:
                if data.decode() == "get_state":
                    component_state = self.get_state()
                    client_connection.sendall(
                        json.dumps(component_state).encode())
                else:
                    deserialized_payload: dict = json.loads(data)

                    response_data = self.process_substance(
                        deserialized_payload)

                    client_connection.sendall(
                        json.dumps(response_data).encode())
            else:
                break

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)

            self.log_info(f"Listening at {self.host}:{self.port}")

            while True:
                client_connection = sock.accept()[0]

                start_new_thread(self.handle_data, (client_connection, ))

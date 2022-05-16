import json
from threading import Thread
from abc import ABC, abstractmethod
from socket import socket, AF_INET, SOCK_STREAM


class BaseComponentServer(ABC):
    host: str
    port: int
    clients: list[socket]

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    @abstractmethod
    def process_substance(self, payload: dict) -> None: pass

    def log_info(self, info: str):
        print(f"{self.__class__.__name__}: {info}")

    @staticmethod
    def connect_client(client_connection: socket, component_server: "BaseComponentServer") -> None:

        with client_connection:
            while True:
                payload = client_connection.recv(1024)

                if payload:
                    # string payload
                    serialized_payload = payload.decode()

                    # converted string payload to dict
                    deserialized_payload: dict = json.loads(serialized_payload)

                    response_data = component_server.process_substance(
                        deserialized_payload)

                    component_server.log_info(response_data)

                    if response_data:
                        client_connection.sendall(
                            json.dumps(response_data).encode())

    def start_client_thread(self, client_connection: socket) -> None:
        client_thread = Thread(
            target=BaseComponentServer.connect_client,
            args=(client_connection, self)
        )
        client_thread.start()

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            self.log_info("Listening at {}:{}".format(self.host, self.port))

            while True:
                client_connection = sock.accept()[0]

                self.start_client_thread(client_connection)

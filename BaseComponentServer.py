import json
from threading import Thread
from abc import ABC, abstractmethod
from socket import socket, AF_INET, SOCK_STREAM
import traceback
from Models.ComponentState import ComponentState


class BaseComponentServer(ABC):
    host: str
    port: int
    clients: list[socket]

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.clients = []

    @abstractmethod
    def process_substance(self, payload: dict) -> ComponentState or None: pass

    def broadcast_response(self, response_data: ComponentState) -> None:
        for client in self.clients:
            client.sendall(str(response_data).encode())

    def log_info(self, info: str):
        print(f"{self.__class__.__name__}: {info}")

    @staticmethod
    def connect_client(client_connection: socket, component_server: "BaseComponentServer") -> None:
        with client_connection:
            try:
                while True:
                    payload = client_connection.recv(1024)

                    if not payload:
                        break

                    # string payload
                    serialized_payload = payload.decode()

                    # converted string payload to dict
                    deserialized_payload: dict = json.loads(serialized_payload)

                    response_data = component_server.process_substance(
                        deserialized_payload)

                    if response_data:
                        component_server.broadcast_response(response_data)
            except Exception as ex:
                component_server.log_info(ex)
                component_server.log_info(
                    f"Some error has occurred: {traceback.print_stack()}")

        component_server.clients.remove(client_connection)

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

                self.clients.append(client_connection)
                self.start_client_thread(client_connection)

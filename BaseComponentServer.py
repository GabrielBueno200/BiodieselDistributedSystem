from abc import ABC, abstractmethod
import json
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class BaseComponentServer(ABC):
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @abstractmethod
    def process_substance(payload: dict): pass

    @staticmethod
    def connect_client(client_connection: socket, component_server: "BaseComponentServer") -> None:
        with client_connection:
            while True:
                payload = client_connection.recv(1024)

                if not payload:
                    break

                # string payload
                serialized_payload = payload.decode('utf-8')

                # converted string payload to dict
                deserialized_payload = json.loads(serialized_payload)

                data_to_response = component_server.process_substance(
                    deserialized_payload)

                if data_to_response is not None:
                    client_connection.sendall(data_to_response)

    def start_client_thread(self, client_connection: "socket") -> None:
        client_thread = Thread(
            target=BaseComponentServer.connect_client,
            args=(client_connection, self)
        )
        client_thread.start()

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))

            while True:
                try:
                    client_connection, client_address = sock.accept()
                    client_ip, client_port = client_address
                    client_address = f"{client_ip}:{client_port}"

                    self.start_client_thread(client_connection)
                except:
                    sock.close()

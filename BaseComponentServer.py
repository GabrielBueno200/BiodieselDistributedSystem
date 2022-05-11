from abc import ABC, abstractmethod
from ast import literal_eval
from socket import socket, AF_INET, SOCK_STREAM


class BaseComponentServer(ABC):
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    @abstractmethod
    def process_substance(payload: dict): pass

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))

            while True:
                client_connection, client_address = sock.accept()
                client_ip, client_port = client_address
                client_address = f"{client_ip}:{client_port}"

                # string payload
                payload = client_connection.recv(1024).decode()

                # converted string payload to dict
                deserialized_payload = literal_eval(payload)

                self.process_substance(deserialized_payload)

                print(f"Received substance from reactor {client_address}")

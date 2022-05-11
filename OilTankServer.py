from socket import socket, AF_INET, SOCK_STREAM


class OilTankServer:
    host: str
    port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def run(self) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.bind((self.host, self.port))
            sock.listen(5)
            print("Listening at {}:{}".format(self.host, self.port))

            while True:
                client_connection, client_address = sock.accept()
                client_ip, client_port = client_address
                client_address = f"{client_ip}:{client_port}"

                payload =client_connection.recv(1024).decode()

                print(payload)

                print(f"Received oil {client_address}")

OilTankServer('localhost', 8082).run()

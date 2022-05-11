from socket import socket, AF_INET, SOCK_STREAM


class DryerServer:
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

                payload = client_connection.recv(1024).decode()

                print(f"Component {payload} {client_address} has been connected")

washing_dryer = DryerServer('localhost', 8087)
ethanol_tank_dryer = DryerServer('localhost', 8088)

washing_dryer.run()
ethanol_tank_dryer.run()
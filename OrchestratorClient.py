from socket import socket, AF_INET, SOCK_STREAM
from Mapping.Ports import ServersPorts
from threading import Thread


class OrchestratrorClient:
    oil_amount = 1

    @staticmethod
    def connect_component(component_server_port: int) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            if (component_server_port == ServersPorts.oil_tank):
                sock.sendall(str(OrchestratrorClient.oil_amount).encode())

            while True:
                pass

    def start(self) -> None:
        components_servers_threads: list[Thread] = []

        for component_port in ServersPorts:
            component_thread = Thread(target=OrchestratrorClient.connect_component,
                                      args=(component_port.value,))

            components_servers_threads.append(component_thread)
            component_thread.start()

        [thread.join() for thread in components_servers_threads]


OrchestratrorClient().start()

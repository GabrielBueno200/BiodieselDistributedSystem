from socket import socket, AF_INET, SOCK_STREAM
from Mapping.Ports import ComponentsServerPorts
from threading import Thread


class OrchestratrorClient:
    @staticmethod
    def connect_component(component_server_port: int):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            while True:
                pass

    def start(self) -> None:
        components_servers_threads = []

        for component_port in ComponentsServerPorts:
            component_thread = Thread(target=OrchestratrorClient.connect_component,
                                      args=component_port,)
            components_servers_threads.append(component_thread)
            component_thread.start()

        for thread in components_servers_threads:
            thread.start()


OrchestratrorClient().start()

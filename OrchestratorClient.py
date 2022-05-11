from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


class OrchestratrorClient:

    @staticmethod
    def connect_component(component_server_port: int):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            while True:
                pass

    def start(self) -> None:
        components_server_ports_mapping = {
            "reactor_server_port": 8080,
            "decanter_server_port": 8081,

            # tanks
            "oil_tank_server_port":  8082,
            "sodium_hydro_tank_server_port": 8083,
            "ethanol_tank_server_port": 8084,
            "biodiesel_tank_server_port": 8085,
            "glycerin_tank_server_port": 8086,

            # dryers
            "washings_dryer_server_port": 8087,
            "ethanol_tank_dryer_server_port": 8088,

            # washings
            "first_washing_server_port": 8089,
            "second_washing_server_port": 8090,
            "third_washing_server_port": 8091
        }

        components_servers_threads = []
        for component_port in components_server_ports_mapping.values():
            component_thread = Thread(target=OrchestratrorClient.connect_component,
                                      args=component_port,)
            components_servers_threads.append(component_thread)
            component_thread.start()

        for thread in components_servers_threads:
            thread.start()


OrchestratrorClient().start()

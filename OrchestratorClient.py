import json
from threading import Thread
from Enums.Ports import ServersPorts
from prettytable import PrettyTable, ALL
from socket import socket, AF_INET, SOCK_STREAM
from Utils.TimeUtilities import call_repeatedly
from Utils.GeneralUtilities import clear_window

from OilTankServer import OilTankServer
from SodiumHydroxideTank import SodiumHydroxideServer
from EthanolTankServer import EthanolTankServer

import sys

class OrchestratorClient:
    time_deposit_oil = 10
    time_deposit_ethanol = 1
    time_deposit_sodium = 1
    cont = 0

    components_state = {
        "oil_tank": {},
        "sodium_hydro_tank": {},
        "ethanol_tank": {},
        "reactor": {},
        "decanter": {},
        "ethanol_tank_dryer": {},
        "glycerin_tank": {},
        "first_washing": {},
        "second_washing": {},
        "third_washing": {},
        "biodiesel_tank_dryer": {},
        "biodiesel_tank": {}
    }

    def __init__(self) -> None:
        self.cont = 0
        self.cancel_future_calls = call_repeatedly(
            interval=1, func=OrchestratorClient.show_components_state)

    @staticmethod
    def connect_component(component_name: str, component_server_port: int) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            if component_server_port == ServersPorts.oil_tank:
                OilTankServer.receive_oil(sock)
                call_repeatedly(OrchestratorClient.time_deposit_oil,
                                OilTankServer.receive_oil, sock)

            elif component_server_port == ServersPorts.sodium_hydro_tank:
                SodiumHydroxideServer.receive_sodium(sock)
                call_repeatedly(OrchestratorClient.time_deposit_sodium,
                                SodiumHydroxideServer.receive_sodium, sock)

            elif component_server_port == ServersPorts.ethanol_tank:
                EthanolTankServer.receive_ethanol(sock)
                call_repeatedly(OrchestratorClient.time_deposit_ethanol,
                                EthanolTankServer.receive_ethanol, sock)

            else:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            while True:
                response = sock.recv(1024)

                OrchestratorClient.components_state[component_name] = json.loads(
                    response)

    @staticmethod
    def show_components_state():
        if OrchestratorClient.components_state:
            clear_window()
            all = []

            for key, value in OrchestratorClient.components_state.items():
                infos = ""
                for info_name, info_value in value.items():
                    infos += f'{info_name}: {info_value}\n'

                all.append([key, infos[:-1]])

            titles = ['Tank', 'Values']

            table = PrettyTable(titles)
            table.align['Values'] = 'l'
            table.add_rows(all)
            table.hrules = ALL
            print(table)

            OrchestratorClient.cont+=1

            with open('stats.txt', 'a') as convert_file:
                convert_file.write(json.dumps(OrchestratorClient.components_state) + '\n')

    
    def count_iterations(self):
        while OrchestratorClient.cont < 3600:
            pass
        self.cancel_future_calls()
        sys.exit()


    def start(self):
        a = Thread(target=self.count_iterations, daemon=True)
        a.start()

        components_servers_threads: list[Thread] = []

        for component_port in ServersPorts:
            component_thread = Thread(target=OrchestratorClient.connect_component,
                                      args=(component_port.name,
                                            component_port.value),
                                      daemon=True)

            component_thread.start()
            components_servers_threads.append(component_thread)

        [thread.join() for thread in components_servers_threads]


OrchestratorClient().start()

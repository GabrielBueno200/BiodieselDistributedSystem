from threading import Thread
from socket import socket, AF_INET, SOCK_STREAM
from xmlrpc.client import Server

from Enums.Ports import ServersPorts
from EthanolTankServer import EthanolTankServer
from SodiumHydroxideTank import SodiumHydroxideServer
from Utils.TimeUtilities import call_repeatedly
from Utils.GeneralUtilities import clear_window
import json
from prettytable import PrettyTable, ALL, FRAME

from OilTankServer import OilTankServer
from ReactorServer import ReactorServer
from SodiumHydroxideTank import SodiumHydroxideServer
from EthanolTankServer import EthanolTankServer

class OrchestratorClient:
    data_payload = 1024
    time_deposit_oil = 10
    time_deposit_ethanol = 1
    time_deposit_sodium = 1
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
        call_repeatedly(interval=1, func=OrchestratorClient.show_components_state)

    @staticmethod
    def connect_component(component_name: str, component_server_port: int) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            if component_server_port == ServersPorts.oil_tank:
                OilTankServer.receive_oil(sock)
                call_repeatedly(OrchestratorClient.time_deposit_oil,
                                OilTankServer.receive_oil, sock)

            if component_server_port == ServersPorts.reactor:
                #sock.sendall("get_state".encode())
                call_repeatedly(1, sock.sendall, "get_state".encode())
            
            if component_server_port == ServersPorts.sodium_hydro_tank:
                SodiumHydroxideServer.receive_sodium(sock)
                call_repeatedly(OrchestratorClient.time_deposit_sodium, 
                                SodiumHydroxideServer.receive_sodium, sock)
                #call_repeatedly(1, sock.sendall, "get_state".encode())

            if component_server_port == ServersPorts.ethanol_tank:
                EthanolTankServer.receive_ethanol(sock)
                call_repeatedly(OrchestratorClient.time_deposit_ethanol,
                                EthanolTankServer.receive_ethanol, sock)
            
            if component_server_port == ServersPorts.decanter:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            if component_server_port == ServersPorts.ethanol_tank_dryer:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            if component_server_port == ServersPorts.glycerin_tank:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            if component_server_port == ServersPorts.biodiesel_tank_dryer:
                call_repeatedly(1, sock.sendall, "get_state".encode())
            
            if component_server_port == ServersPorts.biodiesel_tank:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            if component_server_port == ServersPorts.first_washing:
                call_repeatedly(1, sock.sendall, "get_state".encode())
            
            if component_server_port == ServersPorts.second_washing:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            if component_server_port == ServersPorts.third_washing:
                call_repeatedly(1, sock.sendall, "get_state".encode())

            while True:
                #print(component_name)

                response = sock.recv(OrchestratorClient.data_payload)

                #if response:
                #       print("Orchestrator:", response.decode())

                OrchestratorClient.components_state[component_name] = json.loads(response)

    @staticmethod
    def show_components_state():
        if OrchestratorClient.components_state:
            #clear_window()
            all = []

            for key, value in OrchestratorClient.components_state.items():
                infos = ""
                for info_name, info_value in value.items():
                    infos += f'{info_name}: {info_value}\n'

                all.append([key, infos[:-1]])

            titles = ['Tank', 'Values']

            #print(all, titles)
            tab = PrettyTable(titles)
            tab.align['Values'] = 'l'
            tab.add_rows(all)
            tab.hrules = ALL
            #tab.vrules = FRAME
            print(tab)
            #print(pd.DataFrame(OrchestratorClient.components_state.items()))

    def start(self):
        components_servers_threads: list[Thread] = []

        for component_port in ServersPorts:
            component_thread = Thread(target=OrchestratorClient.connect_component,
                                      args=(component_port.name, component_port.value),
                                      daemon=True)

            component_thread.start()
            components_servers_threads.append(component_thread)

        [thread.join() for thread in components_servers_threads]

OrchestratorClient().start()
from collections import defaultdict
import json
import os
from socket import socket, AF_INET, SOCK_STREAM
from typing import Any
from Enums.Ports import ServersPorts
from threading import Thread
from EthanolTankServer import EthanolTankServer
from SodiumHydroxideTank import SodiumHydroxideServer
from OilTankServer import OilTankServer
from Utils.GeneralUtilities import clear_window
from Utils.TimeUtilities import set_interval
import pandas as pd


class OrchestratrorClient:
    components_state: dict[str, dict[str, Any]] = {}

    @staticmethod
    def connect_component(component_name: str, component_server_port: int) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            if component_server_port == ServersPorts.oil_tank:
                time_deposit_oil = 10
                set_interval(lambda: OilTankServer.receive_oil(
                    sock), time_deposit_oil)

            elif component_server_port == ServersPorts.ethanol_tank:
                time_deposit_ethanol = 1
                set_interval(lambda: EthanolTankServer.receive_ethanol(
                    sock), time_deposit_ethanol)

            elif component_server_port == ServersPorts.sodium_hydro_tank:
                time_deposit_sodium = 1
                set_interval(lambda: SodiumHydroxideServer.receive_sodium(
                    sock), time_deposit_sodium)

            while True:
                sock.recv(1024).decode()

    def start(self) -> None:
        components_servers_threads: list[Thread] = []

        # connect with all component servers iterating in ServersPorts enum,
        # opening a thread for each of them
        for component_port in ServersPorts:
            component_thread = Thread(target=OrchestratrorClient.connect_component,
                                      args=(component_port.name, component_port.value))

            components_servers_threads.append(component_thread)
            component_thread.start()

        [thread.join() for thread in components_servers_threads]


OrchestratrorClient().start()

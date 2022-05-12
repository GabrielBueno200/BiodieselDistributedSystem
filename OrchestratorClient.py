from random import uniform
from socket import socket, AF_INET, SOCK_STREAM
from Enums.Ports import ServersPorts
from threading import Thread
from time import sleep
import json
from Utils.TimeUtilities import set_interval


def deposit_oil(oil_tank_socket: socket):
    oil_amount_by_sec = 0.75
    remaining_oil = uniform(1, 2)
    print(f"Total oil = {remaining_oil}l")

    while remaining_oil > 0:
        oil_to_deposit = 0

        if (remaining_oil - oil_amount_by_sec > 0):
            oil_to_deposit = oil_amount_by_sec
        else:
            oil_to_deposit = remaining_oil

        sleep(1)

        print(f"fueling with: {oil_to_deposit}")

        oil_tank_socket.sendall(json.dumps(
            {"oil_amount": oil_to_deposit}).encode())

        remaining_oil -= oil_to_deposit
    print()


class OrchestratrorClient:
    @staticmethod
    def connect_component(component_server_port: int) -> None:
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(("localhost", component_server_port))

            if (component_server_port == ServersPorts.oil_tank):
                time_to_deposit_oil = 10
                set_interval(lambda: deposit_oil(sock), time_to_deposit_oil)

            while True:
                pass

    def start(self) -> None:
        components_servers_threads: list[Thread] = []

        # connect with all component servers iterating in ServersPorts enum, 
        # opening a thread for each of them
        for component_port in ServersPorts:
            component_thread = Thread(target=OrchestratrorClient.connect_component,
                                      args=(component_port.value,))

            components_servers_threads.append(component_thread)
            component_thread.start()

        [thread.join() for thread in components_servers_threads]


OrchestratrorClient().start()

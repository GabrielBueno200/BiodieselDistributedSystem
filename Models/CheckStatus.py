import json
from socket import AF_INET, SOCK_STREAM, socket

def check_status(port):
    with socket(AF_INET, SOCK_STREAM) as tank_sock:
        tank_sock.connect(("localhost", port))
        tank_sock.sendall("get_state".encode())

        tank_response = tank_sock.recv(1024)

        tank_state = json.loads(tank_response.decode())

        return tank_state


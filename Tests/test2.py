from socket import socket, AF_INET, SOCK_STREAM
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
import json
import time

with socket(AF_INET, SOCK_STREAM) as reactor_sock:
    reactor_sock.connect(("localhost", ServersPorts.reactor))
    payload_to_reactor = {
        "substance_type": SubstanceType.OIL,
        "substance_amount": 0.75
    }

    reactor_sock.sendall(json.dumps(payload_to_reactor).encode())
    time.sleep(60)
    reactor_response = reactor_sock.recv(1024)

    if reactor_response:
        reactor_state = json.loads(reactor_response.decode())
        print(reactor_response)

    reactor_sock.close()
import sys
import json
from Enums.Ports import ServersPorts
from Enums.Substance import SubstanceType
from socket import AF_INET, SOCK_STREAM, socket
from Utils.TimeUtilities import call_repeatedly
from BaseComponentServer import BaseComponentServer


class ThirdWashingServer(BaseComponentServer):
    def __init__(self, host, port) -> None:
        super().__init__(host, port)
        self.substances_outflow = 1.5
        self.loss = 0.025
        self.remaining_solution = 0
        self.cancel_future_calls = call_repeatedly(
            interval=1, func=self.transfer_to_biodiesel_dryer)

    def signal_handler(self, sig, frame):
        self.cancel_future_calls()
        sys.exit(0)

    def get_state(self):
        return {"occupied_capacity": self.remaining_solution}

    def process_substance(self, solution_payload: dict) -> None:
        solution_amount = solution_payload["solution_amount"]
        self.remaining_solution += solution_amount

    def transfer_to_biodiesel_dryer(self):
        if self.remaining_solution > 0:

            substances_to_transfer = 0

            if self.remaining_solution >= self.substances_outflow:
                substances_to_transfer = self.substances_outflow
            else:
                substances_to_transfer = self.remaining_solution

            solutiion_to_send = substances_to_transfer*(1-self.loss)

            with socket(AF_INET, SOCK_STREAM) as component_sock:
                component_sock.connect(
                    ("localhost", ServersPorts.biodiesel_tank_dryer))

                component_sock.sendall(json.dumps(
                    {f"{SubstanceType.SOLUTION}_amount": solutiion_to_send}).encode())

                self.remaining_solution -= substances_to_transfer

                component_sock.recv(self.data_payload)


if __name__ == "__main__":
    ThirdWashingServer('localhost', ServersPorts.third_washing).run()

from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class ReactorServer(BaseComponentServer):
    def process_substance(self, substance_payload: dict):
        substance_type = substance_payload["substance_type"]
        substance_amount = substance_payload["substance_amount"]

        print(f"received {substance_amount}l of {substance_type}")


ReactorServer('localhost', ServersPorts.reactor).run()

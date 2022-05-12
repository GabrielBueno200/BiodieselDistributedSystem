from BaseComponentServer import BaseComponentServer
from Enums.Ports import ServersPorts


class DecanterServer(BaseComponentServer):
    def process_substance(self, substances_payload: dict):
        print(f"Received substance from reactor")


DecanterServer('localhost', ServersPorts.decanter).run()

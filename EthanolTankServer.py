from BaseComponentServer import BaseComponentServer


class EthanolTankServer(BaseComponentServer):
    def process_substance(payload: dict):
        print("received ethanol from decanter")


EthanolTankServer('localhost', 8082).run()

from BaseComponentServer import BaseComponentServer


class OilTankServer(BaseComponentServer):
    def process_substance(payload: dict):
        print(f"Received oil")


OilTankServer('localhost', 8082).run()

from BaseComponentServer import BaseComponentServer


class DecanterServer(BaseComponentServer):
    def process_substance(substances_payload: dict):
        print(f"Received substance from reactor")


DecanterServer('localhost', 8082).run()

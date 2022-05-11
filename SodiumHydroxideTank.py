from BaseComponentServer import BaseComponentServer


class SodiumHydroxideServer(BaseComponentServer):
    print("Received sodium hydroxid from decanter")


SodiumHydroxideServer('localhost', 8083).run()

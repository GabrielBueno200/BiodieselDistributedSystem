from enum import Enum
from Utils.EnumUtilities import EnumDirectValueMeta


class ServersPorts(Enum, metaclass=EnumDirectValueMeta):
    reactor = 8080
    # decanter = 8081

    # tanks
    oil_tank = 8082
    # sodium_hydro_tank = 8083
    ethanol_tank = 8084
    # biodiesel_tank = 8085
    # glycerin_tank = 8086

    # dryers
    # washings_dryer = 8087
    # ethanol_tank_dryer = 8088

    # washings
    # first_washing = 8089
    # second_washing = 8090
    # third_washing = 8091

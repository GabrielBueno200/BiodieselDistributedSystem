from enum import Enum
from Utils.EnumUtilities import EnumDirectValueMeta


class Substance(Enum, metaclass=EnumDirectValueMeta):
    OIL = "oil"
    ETHANOL = "ethanol"
    BIODIESEL = "biodiesel"
    SODIUM_HYDROXIDE = "sodium hydroxide"

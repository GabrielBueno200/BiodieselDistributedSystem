from enum import Enum
from Utils.EnumUtilities import EnumDirectValueMeta


class SubstanceType(Enum, metaclass=EnumDirectValueMeta):
    OIL = "oil"
    ETHANOL = "ethanol"
    BIODIESEL = "biodiesel"
    SODIUM_HYDROXIDE = "sodium hydroxide"

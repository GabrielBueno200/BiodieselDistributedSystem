from enum import Enum

from Utils.EnumUtilities import EnumDirectValueMeta


class SubstanceType(Enum, metaclass=EnumDirectValueMeta):
    OIL = 'oil'
    SODIUM = 'sodium'
    ETHANOL = 'ethanol'
    GLYCERIN = 'glycerin'
    SOLUTION = 'solution'

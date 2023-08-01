from enum import Enum


class SnapSimpEnum(Enum):
    """
    A custom enumeration for usage throughout snap simp to allow the generation of a list of the values contained in the enumeration.
    """

    @classmethod
    def values(cls):
        return list(cls.__members__.values())

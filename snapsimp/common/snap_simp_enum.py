from enum import Enum


class SnapSimpEnum(Enum):
    @classmethod
    def values(cls):
        return list(cls.__members__.values())

from enum import Enum


class AccountTable(Enum):
    BASIC_INFORMATION = 0
    DEVICE_INFORMATION = 1
    DEVICE_HISTORY = 2
    LOGIN_HISTORY = 3

    @classmethod
    def get_table_index(cls, element):
        return element.value
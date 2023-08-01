from enum import Enum


class AccountTableIndicie(Enum):
    """
    The indicies of the tables within an account.html file.
    """

    BASIC_INFORMATION = 0
    DEVICE_INFORMATION = 1
    DEVICE_HISTORY = 2
    LOGIN_HISTORY = 3

    @classmethod
    def get_table_index(cls, element):
        return element.value

from typing import List


class DeviceInformation:
    """
    A device information object holds device info data from a standard account.html file.
    Namely the following properties:

    - make: the make of the current device the account is signed in to
    - model_id: the id of the device the account is currently signed in to
    - model_name: the name of the model of the device the account is currently signed in to
    - user_agent: some kind of debug information Snap exposes.
      This is possibly the closest server of which the device communicates with
    - language: the user's language
    - os_type: the operating system of the device the account is currently signed in to
    - os_version: the version of the operating system of the device the account is currently signed in to
    - connection_type: the type of connections the current device is using such as "WIFI" and "CELL"
    """

    def __init__(
        self,
        make: str,
        model_id: str,
        model_name: str,
        user_agent: str,
        language: str,
        os_type: str,
        os_version: str,
        connection_type: List[str],
    ):
        self.make = make
        self.model_id = model_id
        self.model_name = model_name
        self.user_agent = user_agent
        self.language = language
        self.os_type = os_type
        self.os_version = os_version
        self.connection_type = connection_type

    def __str__(self):
        return (
            f"DeviceInformation(make={self.make}, model_id={self.model_id}, model_name={self.model_name}, "
            f"user_agent={self.user_agent}, language={self.language}, os_type={self.os_type}, "
            f"os_version={self.os_version}, connection_type={self.connection_type})"
        )

    def __repr__(self):
        return self.__str__()

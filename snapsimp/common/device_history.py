from typing import Optional
from datetime import datetime


class DeviceHistory:
    """
    A device history object holds device history data from a standard account.html file.
    Namely the following properties:

    - make: the make of the device such as "Apple"
    - model: the model of the device such as "iPhone"
    - start_time: the time this device's usage began
    - device_type: the device type such as "PHONE"
    """

    def __init__(self, make: str, model: str, start_time: datetime, device_type: str):
        self.make = make
        self.model = model
        self.start_time = start_time
        self.device_type = device_type

    def __str__(self):
        return f"DeviceHistory(make={self.make}, model={self.model}, start_time={self.start_time}, device_type={self.device_type})"

    def __repr__(self):
        return self.__str__()

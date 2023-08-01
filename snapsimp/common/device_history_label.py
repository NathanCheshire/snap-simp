from common.snap_simp_enum import SnapSimpEnum


class DeviceHistoryLabel(SnapSimpEnum):
    """
    Valid labels used for parsing a device history row from the device history table of an account.html file.
    """

    MAKE = "Make:"
    MODEL = "Model:"
    START_TIME = "Start Time:"
    DEVICE_TYPE = "Device Type:"

from common.snap_simp_enum import SnapSimpEnum


class LoginHistoryLabel(SnapSimpEnum):
    """
    Valid labels used for parsing a login history row from the login history table of an account.html file.
    """

    IP = "IP:"
    COUNTRY = "Country:"
    CREATED = "Created:"
    STATUS = "Status:"
    DEVICE = "Device:"

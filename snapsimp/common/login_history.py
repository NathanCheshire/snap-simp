from datetime import datetime
import ipaddress


class LoginHistory:
    """
    A login history object holds login history data from a standard account.html file.
    Namely the following properties:

    - ip: the ip of the login
    - country: the country of the login's origin
    - created: the time of the login
    - status: the status of the login
    - device: the device the login was performed on
    """

    def __init__(
        self, ip: str, country: str, created: datetime, status: str, device: str
    ):
        self.ip = ipaddress.ip_address(ip)
        self.country = country
        self.created = created
        self.status = status
        self.device = device
        self.validate_ip()

    def validate_ip(self) -> None:
        if not isinstance(self.ip, (ipaddress.IPv4Address, ipaddress.IPv6Address)):
            raise ValueError(f"Invalid IP address: {self.ip}")

    def __str__(self):
        return f"LoginHistory(ip={self.ip}, country={self.country}, created={self.created}, status={self.status}, device={self.device})"

    def __repr__(self):
        return self.__str__()

from datetime import datetime

from snaps.snap_type import SnapType
from snaps.snap_direction import SnapDirection

class Snap:
    def __init__(self, sender, type, timestamp, direction=None):
        self.sender = sender
        self.type = SnapType(type)
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %Z')
        self.direction = direction if direction else None

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = type

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, direction: SnapDirection):
        if direction is not None:
            if isinstance(direction, SnapDirection):
                self._direction = direction
            else:
                raise TypeError("direction must be an instance of SnapDirection Enum")
        else:
            self._direction = None

    def __repr__(self):
        return f"Snap(sender='{self.sender}', type='{self.type}', timestamp='{self.timestamp}', direction={self.direction})"

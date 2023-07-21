from datetime import datetime
from enum import Enum

class SnapType(Enum):
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'

class Snap:
    def __init__(self, sender, type, timestamp):
        self.sender = sender
        self.type = SnapType(type)
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %Z')

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

    def __repr__(self):
        return f"Snap(sender='{self.sender}', type='{self.type}', timestamp='{self.timestamp}')"

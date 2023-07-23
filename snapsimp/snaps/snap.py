from datetime import datetime

from snaps.snap_type import SnapType

class Snap:
    def __init__(self, sender, receiver, type, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.type = SnapType(type)
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S %Z')

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, sender):
        self._sender = sender

    @property
    def receiver(self):
        return self._receiver

    @receiver.setter
    def receiver(self, receiver):
        self._receiver = receiver

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
        return f"Snap(sender='{self.sender}', receiver='{self.receiver}', type='{self.type}', timestamp='{self.timestamp}')"

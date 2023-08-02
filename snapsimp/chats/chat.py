from datetime import datetime

from chats.chat_type import ChatType


class Chat:
    """
    A chat represents a singular chat of a specific type sent from a singular sender to a singular receiver.
    """

    def __init__(self, sender, receiver, type, text, timestamp):
        """
        Creates a new Chat object.

        :param sender: the username of the sender of the chat
        :param receiver: the username of the receiver of the chat
        :param type: the chat type such as video or image
        :param text: the string content of the text if the type is of text
        :param timestamp: the time at which the chat was sent by the sender's device
        """
        self.sender = sender
        self.receiver = receiver
        self.type = ChatType(type)
        self.text = text
        self.timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S %Z")

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
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = text

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        self._timestamp = timestamp

    def __repr__(self):
        return f"Chat(sender='{self.sender}', receiver='{self.receiver}', type={self.type}, timestamp='{self.timestamp}', text='{self.text}')"

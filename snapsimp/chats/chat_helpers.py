from datetime import datetime
from chats.chat_type import ChatType


def json_chat_encoder(obj):
    """
    A helper function to encode complex objects for JSON serialization.

    :param obj: the object to encode
    :return: a dictionary representing the object
    """

    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ChatType):
        return obj.value
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

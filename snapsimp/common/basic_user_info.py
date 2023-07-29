from datetime import datetime


class BasicUserInfo:
    """
    BasicUserInfo as parsed from the 'account.html' file. 

    :param username: The Snapchat username of the user.
    :param name: The name of the user (typically not equal to the username).
    :param creation_date: The creation date of the user's Snapchat account.

    :type username: str
    :type name: str
    :type creation_date: str

    The creation_date is a string in the format '%Y-%m-%d %H:%M:%S %Z' and it will be converted 
    to a datetime object upon object instantiation.
    """

    def __init__(self, username: str, name: str, creation_date: str):
        self.username = username
        self.name = name
        self.creation_date = datetime.strptime(
            creation_date, '%Y-%m-%d %H:%M:%S %Z')

    def __str__(self):
        return f"BasicUserInfo(username='{self.username}', name='{self.name}', creation_date='{self.creation_date}')"

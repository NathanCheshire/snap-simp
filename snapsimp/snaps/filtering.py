from typing import List, Set, Tuple
from snaps.snap import Snap
import snaps.statistics as stats
from snaps.snap_type import SnapType


def get_snaps_by_sending_user(snaps: List[Snap], username: str) -> List[Snap]:
    """
    Returns all snaps sent by a specific user from the given list.

    :param snaps: The list of Snap objects to analyze
    :param username: The username of the sender
    :return: a list of Snap objects sent by the specified user
    """

    return [snap for snap in snaps if snap.sender == username]


def get_snaps_by_receiving_user(snaps: List[Snap], username: str) -> List[Snap]:
    """
    Returns all snaps received by a specific user from the given list.

    :param snaps: The list of Snap objects to analyze
    :param username: The username of the receiver
    :return: a list of Snap objects received by the specified user
    """

    return [snap for snap in snaps if snap.receiver == username]


def get_top_sender_username(snaps: List[Snap]) -> str:
    """
    Returns the username of the person whos name appears on the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the username of the person who sends/receives the most snaps to/from you
    """

    sorted_sender_username_dict, _ = stats.get_count(snaps)
    return next(iter(sorted_sender_username_dict))


def get_top_receiver_username(snaps: List[Snap]) -> str:
    """
    Returns the username of the person whos name appears on the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the username of the person who sends/receives the most snaps to/from you
    """

    _, sorted_receiver_username_dict = stats.get_count(snaps)
    return next(iter(sorted_receiver_username_dict))


def get_snaps_by_top_sender(snaps: List[Snap]) -> List[Snap]:
    """
    Returns a subset of the provided list of snaps containing only the snaps from the top sender

    :param snaps: the list of snaps
    :return: a list of snaps containing the snaps from the top sender
    """

    top_sender = get_top_sender_username(snaps)
    return get_snaps_by_sending_user(snaps, top_sender)


def get_snaps_by_top_receiver(snaps: List[Snap]) -> List[Snap]:
    """
    Returns a subset of the provided list of snaps containing only the snaps to the top receiver

    :param snaps: the list of snaps
    :return: a list of snaps containing the snaps to the top receiver
    """

    top_receiver = get_top_receiver_username(snaps)
    return get_snaps_by_receiving_user(snaps, top_receiver)


def filter_snaps_by_type(snaps: List[Snap]) -> Tuple[List[Snap], List[Snap]]:
    """
    Separates a list of Snap objects into two lists: one for images and one for videos.

    :param snaps: A list of Snap objects
    :return: A tuple containing two lists of Snap objects: the first for image snaps and the second for video snaps
    """

    image_snaps = [snap for snap in snaps if snap.type == SnapType.IMAGE]
    video_snaps = [snap for snap in snaps if snap.type == SnapType.VIDEO]

    return image_snaps, video_snaps


def get_unique_sending_usernames(snaps: List[Snap]) -> Set[str]:
    """
    Returns all unique sender usernames from the list of Snap objects.

    :param snaps: a list of Snap objects
    :return: a set of unique usernames
    """

    sender_names = {snap.sender for snap in snaps}
    return sender_names


def get_unique_receiving_usernames(snaps: List[Snap]) -> Set[str]:
    """
    Returns all unique receiver usernames from the list of Snap objects.

    :param snaps: a list of Snap objects
    :return: a set of unique usernames
    """

    receiver_names = {snap.receiver for snap in snaps}
    return receiver_names

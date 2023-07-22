from typing import  List, Set, Tuple
from snaps.snap import Snap
import snaps.statistics as stats
from snaps.snap_type import SnapType
from snaps.snap_direction import SnapDirection


def get_snaps_by_user(snaps: List[Snap], username: str, direction: SnapDirection) -> List[Snap]:
    """
    Returns all snaps sent/received by a specific user from the given list.

    :param snaps: The list of Snap objects to analyze
    :param username: The username of the sender/receiver
    :return: A list of Snap objects sent/received by/from the specified user
    """

    if direction == SnapDirection.SENT:
        return [snap for snap in snaps if snap.sender == username]
    else:
        return [snap for snap in snaps if snap.receiver == username]


def get_top_username(snaps: List[Snap], direction: SnapDirection) -> str:
    """
    Returns the username of the person whos name appears on the most snaps of the provided list.

    :param snaps: the list of snaps
    :param direction: the direction of the snap
    :return: the username of the person who sends/receives the most snaps to/from you
    """

    frequency = stats.compute_snap_count(snaps, direction)
    return next(iter(frequency))


def get_snaps_by_top_username(snaps: List[Snap], direction: SnapDirection) -> List[Snap]:
    """
    Returns a subset of the provided list of snaps containing only the snaps to/from the highest receiver/sender.

    :param snaps: the list of snaps
    :param direction: the direction of the snap to get the top username of, i.e. top sender to you or top receiver from you
    :return: a list of snaps containing the snaps to/from the top receiver/sender. If the provided list was snaps
    received by you, the subset would contain the snaps sent from the person who snaps you the most. If the provided
    list was snaps sent by you, the subset would contain the snaps received from the person who you snap the most.
    """

    top_sender_or_receiver = get_top_username(snaps, direction)
    return get_snaps_by_user(snaps, top_sender_or_receiver, direction)


def filter_snaps_by_type(snaps: List[Snap]) -> Tuple[List[Snap], List[Snap]]:
    """
    Separates a list of Snap objects into two lists: one for images and one for videos.

    :param snaps: A list of Snap objects
    :return: A tuple containing two lists of Snap objects: the first for image snaps and the second for video snaps
    """

    image_snaps = [snap for snap in snaps if snap.type == SnapType.IMAGE]
    video_snaps = [snap for snap in snaps if snap.type == SnapType.VIDEO]

    return image_snaps, video_snaps


def get_unique_usernames(snaps: List[Snap], direction: SnapDirection) -> Set[str]:
    """
    Returns all unique sender/receiver usernames from the list of Snap objects.

    :param snaps: A list of Snap objects
    :param direction: the direction of the snaps
    :return: A set of unique sender usernames.
    """

    if direction == SnapDirection.SENT:
        return {snap.sender for snap in snaps}
    else:
        return {snap.receiver for snap in snaps}


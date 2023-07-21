from typing import Dict, List, Set
from collections import Counter
import snaps.filtering as filtering
from snaps.snap import Snap, SnapType


def compute_sender_frequency(snaps: List[Snap]) -> Dict[str, int]:
    """
    Computes and returns a dictionary detailing the frequency of a particular sender/receiver.

    Example returned schema:
    {
        "mybestfriend": 143,
        "mysister": 22,
        "mycousin": 15
    }

    :param snaps: the list of snaps to compute the sender frequency of
    :return: a dictionary detailing the frequency of a particular sender/receiver
    """

    username_counter = Counter(snap.sender for snap in snaps)
    sorted_username_counts = sorted(username_counter.items(), key=lambda item: item[1], reverse=True)
    sorted_username_dict = dict(sorted_username_counts)
    return sorted_username_dict


def get_snap_type_frequency(snaps: List[Snap]) -> Dict[SnapType, int]:
    """
    Count the number of each type of snap in the given list.

    :param snaps: The list of Snap objects to analyze
    :return: A dictionary mapping each snap type to its frequency
    """

    type_counts = Counter([snap.type for snap in snaps])
    return type_counts


def get_image_to_video_ratio_by_username(snaps: List[Snap], username: str) -> float:
    """
    Returne the image to video snap ratio of the provided username.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list.
    """

    snaps_from_user = filtering.get_snaps_by_user(snaps, username)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_from_user)
    return len(image_snaps) / len(video_snaps)


def get_image_to_video_ratio_by_top_username(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of the user with the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of the user with the most snaps in the list. For example,
    if this was the snaps you received, this would return the ratio of image to video snaps of the person
    who sent you the most snaps
    """

    return get_image_to_video_ratio_by_username(snaps, filtering.get_top_username(snaps))

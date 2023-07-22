from datetime import timedelta
from typing import Dict, List, Set
from collections import Counter
import snaps.filtering as filtering
from snaps.snap import Snap
import snaps.filtering as filtering
from common.date_range import DateRange
from snaps.snap_type import SnapType
from common.descriptive_stats import DescriptiveStatsTimedelta
from snaps.snap_direction import SnapDirection

def compute_snap_count(snaps: List[Snap], direction: SnapDirection) -> Dict[str, int]:
    """
    Computes and returns a dictionary detailing the count of each unique sender/receiver.

    Example returned schema:
    {
        "mybestfriend": 143,
        "mysister": 22,
        "mycousin": 15
    }

    :param snaps: the list of snaps to compute the sender count of
    :param direction: the direction to compute the snap count of, sent/received
    :return: a dictionary detailing the count of a particular sender/receiver
    """

    if direction == SnapDirection.SENT:
        username_count = Counter(snap.sender for snap in snaps)
    else:
        username_count = Counter(snap.receiver for snap in snaps)

    sorted_username_counts = sorted(username_count.items(), key=lambda item: item[1], reverse=True)
    sorted_username_dict = dict(sorted_username_counts)
    return sorted_username_dict


def get_snap_type_count(snaps: List[Snap]) -> Dict[SnapType, int]:
    """
    Count the number of each type of snap in the given list.

    :param snaps: The list of Snap objects to analyze
    :return: A dictionary mapping each snap type to its count
    """

    type_counts = Counter([snap.type for snap in snaps])
    return type_counts


def get_image_to_video_ratio_by_username(snaps: List[Snap], username: str, direction: SnapDirection) -> float:
    """
    Returne the image to video snap ratio of the provided username.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list.
    :param direction: the direction for computing teh image to video ratio of, such as the ratio of sent images to videos
    or the ratio of received images to videos of a particular user
    """


    snaps_by_username = filtering.get_snaps_by_user(snaps, username, direction)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_by_username)
    return len(image_snaps) / len(video_snaps)

# todo need direction
def get_image_to_video_ratio_by_top_username(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of the user with the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of the user with the most snaps in the list. For example,
    if this was the snaps you received, this would return the ratio of image to video snaps of the person
    who sent you the most snaps
    """

    return get_image_to_video_ratio_by_username(snaps, filtering.get_top_username(snaps))


def get_number_of_snaps_by_username(snaps: List[Snap], username: str):
    """
    Returns the number of snaps by by the following username in the provided set.

    :param snaps: the list of snaps
    :param username: the username to filter on
    """

    return len(filtering.get_snaps_by_sending_user(snaps, username))


def order_by_time_in_ascending_order(snaps: List[Snap]) -> List[Snap]:
    return sorted(snaps, key=lambda snap: snap.timestamp)


def order_by_time_in_descending_order(snaps: List[Snap]) -> List[Snap]:
    return sorted(snaps, key=lambda snap: snap.timestamp, reverse=True)


def get_date_range(snaps: List[Snap]) -> DateRange:
    time_ordered = time_ordered = order_by_time_in_ascending_order(snaps)
    assert len(time_ordered) >= 2
    return DateRange(time_ordered[0].timestamp, time_ordered[-1].timestamp)


def get_duration_of_snap_with_top_snapper(snaps: List[Snap]) -> timedelta:
    top_user_snaps = filtering.get_snaps_by_top_username(snaps)
    return get_date_range(top_user_snaps).duration()


def calculate_descriptive_stats_between_snaps_of_top_user(sent_snaps: List[Snap], received_snaps: List[Snap]) -> DescriptiveStatsTimedelta:
    # first we'll need to merge these lists and sort them by time, then we'll need to eliminate ones with
    # the same sender with a lower time so basically we'll have a list of the most recent alternating snaps
    # then we'll compute the times differences between all there, then we can average it

    top_to_user = filtering.get_top_username(sent_snaps)
    top_from_user = filtering.get_top_username(received_snaps)
    print(top_to_user, top_from_user)
    assert top_to_user == top_from_user

    top_sent_to_snaps = filtering.get_snaps_by_sending_user(sent_snaps, top_to_user)
    top_received_from_snaps = filtering.get_snaps_by_sending_user(received_snaps, top_from_user)

    # place in ordering
    all_top_snaps = top_sent_to_snaps + top_received_from_snaps
    time_ordered = order_by_time_in_ascending_order(all_top_snaps)

    # now we'll need a two running variables as we loop through
    # we'll need the most recent time and the most recent 
    # when sender

    for snap in time_ordered[0:100]:
        print(snap)

    return 0.0

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
from statistics import mean

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
    :param direction: the direction for computing the image to video ratio of, such as the ratio of sent images to videos
    or the ratio of received images to videos of a particular user
    """

    snaps_by_username = filtering.get_snaps_by_user(snaps, username, direction)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_by_username)
    return len(image_snaps) / len(video_snaps)

def get_image_to_video_ratio_by_top_username(snaps: List[Snap], direction: SnapDirection) -> float:
    """
    Returns the image to video snap ratio of the user with the most snaps of the provided list.

    :param snaps: the list of snaps
    :param direction: the direction to compute the image to video snap ratio of
    :return: the image to video snap ratio of the user with the most snaps in the list. For example,
    if this was the snaps you received, this would return the ratio of image to video snaps of the person
    who sent you the most snaps
    """

    return get_image_to_video_ratio_by_username(snaps, filtering.get_top_username(snaps), direction)


def get_number_of_snaps_by_username(snaps: List[Snap], username: str):
    """
    Returns the number of snaps by by the following username in the provided set.

    :param snaps: the list of snaps
    :param username: the username to filter on
    """

    return len(filtering.get_snaps_by_sending_user(snaps, username))


def order_by_time_in_ascending_order(snaps: List[Snap]) -> List[Snap]:
    """
    Returns the provided snap list after sorting into ascending order by the send time.

    :param snaps: the list of snaps to sort into ascending order by send time
    """

    return sorted(snaps, key=lambda snap: snap.timestamp)


def order_by_time_in_descending_order(snaps: List[Snap]) -> List[Snap]:
    """
    Returns the provided snap list after sorting into descending order by the send time.

    :param snaps: the list of snaps to sort into descending order by send time
    """

    return sorted(snaps, key=lambda snap: snap.timestamp, reverse=True)


def get_date_range(snaps: List[Snap]) -> DateRange:
    """
    Returns the date range of the provided list of snaps meaning the range between which all the snaps fall into.

    :param snaps: the list of snaps
    """

    time_ordered = time_ordered = order_by_time_in_ascending_order(snaps)
    if len(time_ordered) < 2:
        raise AssertionError("Cannot construct a date range from less than 2 snaps")
    return DateRange(time_ordered[0].timestamp, time_ordered[-1].timestamp)


def get_duration_of_snap_with_top_snapper(snaps: List[Snap], direction: SnapDirection) -> timedelta:
    """
    Returns the duration of the snaps sent or received from the top snapper from within the list.
    For example, if a snap direction of received is provided, the returned time delta will convey how long
    you have been receiving snaps from the top person who snaps you in this list.

    :param snaps: the list of snaps
    :param direction: the direction of snaps
    """

    top_user_snaps = filtering.get_snaps_by_top_username(snaps, direction)
    return get_date_range(top_user_snaps).duration()


def calculate_descriptive_stats_between_snaps_of_top_user(sent_snaps: List[Snap], received_snaps: List[Snap]) -> DescriptiveStatsTimedelta:
    """
    Computes and returns the descriptive stats between the top person you send and receive snaps to/from.
    The provided lists are expected to have the same top user from them meaning you send the most
    snaps to the person who sends you the most. The descriptive stats include a minimum, average, and maximum amount of time
    between you sending a snap or series of snaps and the receipient replying AND the receipient sending you a snap or
    series of snaps and you replying.

    :param sent_snaps: the snaps you have sent
    :param received_snaps: the snaps you have received
    """

    top_to_user = filtering.get_top_username(sent_snaps, SnapDirection.RECEIVED)
    top_from_user = filtering.get_top_username(received_snaps, SnapDirection.SENT)

    if top_to_user != top_from_user:
        raise AssertionError(f"Top from snapper must be equal to top to snapper, from sent and received snaps found that top sender was {top_from_user} while top receiver was {top_to_user}")

    top_sent_to_snaps = filtering.get_snaps_by_user(sent_snaps, top_to_user, SnapDirection.RECEIVED)
    top_received_from_snaps = filtering.get_snaps_by_user(received_snaps, top_from_user, SnapDirection.SENT)

    all_top_snaps = top_sent_to_snaps + top_received_from_snaps
    time_ordered = order_by_time_in_ascending_order(all_top_snaps)

    current_sender = time_ordered[0].sender
    current_time = time_ordered[0].timestamp
    awaiting_response_periods: List[DateRange] = []

    for snap in time_ordered:
        if current_sender == snap.sender:
            current_time = snap.timestamp
            continue
        else:
            current_sender = snap.sender
            new_time = snap.timestamp
            awaiting_response_periods.append(DateRange(current_time, new_time))
            current_time = new_time


    awaiting_response_times = [p2.start_date - p1.end_date for p1, p2 in zip(awaiting_response_periods, awaiting_response_periods[1:])]

    min_diff = min(awaiting_response_times)
    max_diff = max(awaiting_response_times)
    avg_diff = timedelta(seconds=mean([diff.total_seconds() for diff in awaiting_response_times]))

    return DescriptiveStatsTimedelta(min_diff, avg_diff, max_diff)

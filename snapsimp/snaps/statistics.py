from datetime import timedelta
from datetime import datetime
from typing import Dict, List, Tuple
from collections import Counter
import snaps.filtering as filtering
from snaps.snap import Snap
import snaps.filtering as filtering
from common.date_range import DateRange
from snaps.snap_type import SnapType
from common.time_helpers import generate_ordered_date_range

def compute_snap_count(snaps: List[Snap]) -> Tuple[Dict[str, int], Dict[str, int]]:
    """
    Computes and returns a dictionary detailing the count of each unique sender and receiver.

    Example returned schema:
    (
        {
            "mybestfriend": 143,
            "mysister": 22,
            "mycousin": 15
        }
        {
            "mybestfriend": 143,
            "mysister": 22,
            "mycousin": 15
        }
    )

    :param snaps: the list of snaps to compute the sender count of
    :return: a tuple containing two dictionaries, the first details the snap counts
    of the sender usernames and the second details the snap counts of the receiving usernames
    """

    sender_username_count = Counter(snap.sender for snap in snaps)
    receiver_username_count = Counter(snap.receiver for snap in snaps)

    sorted_sender_username_counts = sorted(sender_username_count.items(), key=lambda item: item[1], reverse=True)
    sorted_receiver_username_counts = sorted(receiver_username_count.items(), key=lambda item: item[1], reverse=True)

    sorted_sender_username_dict = dict(sorted_sender_username_counts)
    sorted_receiver_username_dict = dict(sorted_receiver_username_counts)

    return sorted_sender_username_dict, sorted_receiver_username_dict


def get_snap_type_count(snaps: List[Snap]) -> Dict[SnapType, int]:
    """
    Count the number of each type of snap in the given list, that of video or image.

    todo example schema here

    :param snaps: The list of Snap objects to analyze
    :return: A dictionary mapping each snap type to its count
    """

    type_counts = Counter([snap.type for snap in snaps])
    return type_counts


def get_image_to_video_ratio_by_sending_user(snaps: List[Snap], username: str) -> float:
    """
    Returns the image to video snap ratio of the provided sending user.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list
    """

    snaps_by_username = filtering.get_snaps_by_sending_user(snaps, username)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_by_username)
    return len(image_snaps) / len(video_snaps)


def get_image_to_video_ratio_by_receiving_user(snaps: List[Snap], username: str) -> float:
    """
    Returns the image to video snap ratio of the provided receiving user.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list
    """

    snaps_by_username = filtering.get_snaps_by_receiving_user(snaps, username)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_by_username)
    return len(image_snaps) / len(video_snaps)


def get_image_to_video_ratio_by_top_sender(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of top sender of snaps from within the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of top sender of snaps from within the provided list
    """

    return get_image_to_video_ratio_by_sending_user(snaps, filtering.get_top_sender_username(snaps))


def get_image_to_video_ratio_by_top_receiver(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of top recipient of snaps from within the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of top recipient of snaps from within the provided list
    """

    return get_image_to_video_ratio_by_receiving_user(snaps, filtering.get_top_receiver_username(snaps))


def get_number_of_snaps_by_sender(snaps: List[Snap], username: str):
    """
    Returns the number of snaps the provided user sent.

    :param snaps: the list of snaps
    :param username: the username to filter on
    :return: the number of snaps the provided user sent
    """

    return len(filtering.get_snaps_by_sending_user(snaps, username))


def get_number_of_snaps_by_receiver(snaps: List[Snap], username: str):
    """
    Returns the number of snaps the provided user received.

    :param snaps: the list of snaps
    :param username: the username to filter on
    :return: the number of snaps the provided user received
    """

    return len(filtering.get_snaps_by_receiving_user(snaps, username))


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


def get_duration_of_snap_with_top_sender(snaps: List[Snap]) -> timedelta:
    """
    Returns the duration of the snaps sent by the top sender from within the list.

    :param snaps: the list of snaps
    """

    top_sender_snaps = filtering.get_snaps_by_top_sender(snaps)
    return get_date_range(top_sender_snaps).duration()


def get_duration_of_snap_with_top_receiver(snaps: List[Snap]) -> timedelta:
    """
    Returns the duration of the snaps received by the top receiver from within the list.

    :param snaps: the list of snaps
    """

    top_receiver_snaps = filtering.get_snaps_by_top_receiver(snaps)
    return get_date_range(top_receiver_snaps).duration()


def get_days_top_sender_did_not_send(snaps: List[Snap]) -> List[datetime]:
    days_top_sender_sent = get_days_top_sender_sent(snaps)

    min_date = min(days_top_sender_sent)
    max_date = max(days_top_sender_sent)

    all_days_sorted = generate_ordered_date_range(min_date, max_date)
    days_top_sender_did_not_send = list(set(all_days_sorted) - set(days_top_sender_sent))
    days_top_sender_did_not_send_sorted = sorted(days_top_sender_did_not_send)

    return days_top_sender_did_not_send_sorted


def get_days_top_receiver_did_not_receive(snaps: List[Snap]) -> List[datetime]:
    days_top_receiver_received = get_days_top_receiver_received(snaps)

    min_date = min(days_top_receiver_received)
    max_date = max(days_top_receiver_received)

    all_days_sorted = generate_ordered_date_range(min_date, max_date)
    days_top_receiver_did_not_receive = list(set(all_days_sorted) - set(days_top_receiver_received))
    days_top_receiver_did_not_receive_sorted = sorted(days_top_receiver_did_not_receive)

    return days_top_receiver_did_not_receive_sorted


def get_days_top_sender_sent(snaps: List[Snap]) -> List[datetime]:
    top_sender_snaps = filtering.get_snaps_by_top_sender(snaps)
    days_top_sender_sent = {snap.timestamp.date() for snap in top_sender_snaps}
    return sorted(list(days_top_sender_sent))


def get_days_top_receiver_received(snaps: List[Snap]) -> List[datetime]:
    top_receiver_snaps = filtering.get_snaps_by_top_receiver(snaps)
    days_top_receiver_received = {snap.timestamp.date() for snap in top_receiver_snaps}
    return sorted(list(days_top_receiver_received))


# this method should accept a conversation object
# def calculate_descriptive_stats_between_snaps_of_top_user(sent_snaps: List[Snap], received_snaps: List[Snap]) -> DescriptiveStatsTimedelta:
#     """
#     Computes and returns the descriptive stats between the top person you send and receive snaps to/from.
#     The provided lists are expected to have the same top user from them meaning you send the most
#     snaps to the person who sends you the most. The descriptive stats include a minimum, average, and maximum amount of time
#     between you sending a snap or series of snaps and the receipient replying AND the receipient sending you a snap or
#     series of snaps and you replying.

#     :param sent_snaps: the snaps you have sent
#     :param received_snaps: the snaps you have received
#     """

#     top_to_user = filtering.get_top_username(sent_snaps, SnapDirection.RECEIVED)
#     top_from_user = filtering.get_top_username(received_snaps, SnapDirection.SENT)

#     if top_to_user != top_from_user:
#         raise AssertionError(f"Top from snapper must be equal to top to snapper, from sent and received snaps found that top sender was {top_from_user} while top receiver was {top_to_user}")

#     top_sent_to_snaps = filtering.get_snaps_by_user(sent_snaps, top_to_user, SnapDirection.RECEIVED)
#     top_received_from_snaps = filtering.get_snaps_by_user(received_snaps, top_from_user, SnapDirection.SENT)

#     all_top_snaps = top_sent_to_snaps + top_received_from_snaps
#     time_ordered = order_by_time_in_ascending_order(all_top_snaps)

#     current_sender = time_ordered[0].sender
#     current_time = time_ordered[0].timestamp
#     awaiting_response_periods: List[DateRange] = []

#     for snap in time_ordered:
#         if current_sender == snap.sender:
#             current_time = snap.timestamp
#             continue
#         else:
#             current_sender = snap.sender
#             new_time = snap.timestamp
#             awaiting_response_periods.append(DateRange(current_time, new_time))
#             current_time = new_time


#     awaiting_response_times = [p2.start_date - p1.end_date for p1, p2 in zip(awaiting_response_periods, awaiting_response_periods[1:])]

#     min_diff = min(awaiting_response_times)
#     max_diff = max(awaiting_response_times)
#     avg_diff = timedelta(seconds=mean([diff.total_seconds() for diff in awaiting_response_times]))

#     return DescriptiveStatsTimedelta(min_diff, avg_diff, max_diff)

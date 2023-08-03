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
from chats.chat import Chat
from chats.chat_type import ChatType


def get_count(
    snaps_or_chats: List[Snap | Chat],
) -> Tuple[Dict[str, int], Dict[str, int]]:
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

    :param snaps_or_chats: the list of snaps or chats to compute the sender count of
    :return: a tuple containing two dictionaries, the first details the snap or chat counts
    of the sender usernames and the second details the snap or chat counts of the receiving usernames
    """

    sender_username_count = Counter(item.sender for item in snaps_or_chats)
    receiver_username_count = Counter(item.receiver for item in snaps_or_chats)

    sorted_sender_username_counts = sorted(
        sender_username_count.items(), key=lambda item: item[1], reverse=True
    )
    sorted_receiver_username_counts = sorted(
        receiver_username_count.items(), key=lambda item: item[1], reverse=True
    )

    sorted_sender_username_dict = dict(sorted_sender_username_counts)
    sorted_receiver_username_dict = dict(sorted_receiver_username_counts)

    return sorted_sender_username_dict, sorted_receiver_username_dict


def get_type_count(snaps_or_chats: List[Snap | Chat]) -> Dict[SnapType | ChatType, int]:
    """
    Count the number of each type of snap or chat in the given list, that of video or image for snaps or text or media for chats.

    Example:
    {
        "IMAGE": 1984,
        "VIDEO": 5150
    }

    :param snaps_or_chats: The list of Snap or Chat objects to analyze
    :return: A dictionary mapping each snap or chat type to its count
    """

    type_counts = Counter([snap.type for snap in snaps_or_chats])
    return type_counts


def get_image_to_video_ratio_by_sending_user(snaps: List[Snap], username: str) -> float:
    """
    Returns the image to video snap ratio of the provided sending user.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list
    """

    snaps_by_username = filtering.get_by_sending_user(snaps, username)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_by_username)
    return len(image_snaps) / len(video_snaps)


def get_text_to_media_ratio_by_sending_user(chats: List[Chat], username: str) -> float:
    """
    Returns the text to media chat ratio of the provided sending user.

    :param snaps: the list of chats
    :param username: the username to return the text to media chat ratio from within the provided chats list
    """

    chats_by_username = filtering.get_by_sending_user(chats, username)
    text_chats, media_chats = filtering.filter_snaps_by_type(chats_by_username)
    return len(text_chats) / len(media_chats)


def get_image_to_video_ratio_by_receiving_user(
    snaps: List[Snap], username: str
) -> float:
    """
    Returns the image to video snap ratio of the provided receiving user.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list
    """

    snaps_by_username = filtering.get_by_receiving_user(snaps, username)
    image_snaps, video_snaps = filtering.filter_snaps_by_type(snaps_by_username)
    return len(image_snaps) / len(video_snaps)


def get_image_to_video_ratio_by_top_sender(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of top sender of snaps from within the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of top sender of snaps from within the provided list
    """

    return get_image_to_video_ratio_by_sending_user(
        snaps, filtering.get_top_sender_username(snaps)
    )


def get_image_to_video_ratio_by_top_receiver(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of top recipient of snaps from within the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of top recipient of snaps from within the provided list
    """

    return get_image_to_video_ratio_by_receiving_user(
        snaps, filtering.get_top_receiver_username(snaps)
    )


def get_number_of_snaps_by_sender(snaps: List[Snap], username: str):
    """
    Returns the number of snaps the provided user sent.

    :param snaps: the list of snaps
    :param username: the username to filter on
    :return: the number of snaps the provided user sent
    """

    return len(filtering.get_by_sending_user(snaps, username))


def get_number_of_snaps_by_receiver(snaps: List[Snap], username: str):
    """
    Returns the number of snaps the provided user received.

    :param snaps: the list of snaps
    :param username: the username to filter on
    :return: the number of snaps the provided user received
    """

    return len(filtering.get_by_receiving_user(snaps, username))


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

    top_sender_snaps = filtering.get_by_top_sender(snaps)
    return get_date_range(top_sender_snaps).duration()


def get_duration_of_snap_with_top_receiver(snaps: List[Snap]) -> timedelta:
    """
    Returns the duration of the snaps received by the top receiver from within the list.

    :param snaps: the list of snaps
    """

    top_receiver_snaps = filtering.get_by_top_receiver(snaps)
    return get_date_range(top_receiver_snaps).duration()


def get_days_top_sender_did_not_send(snaps: List[Snap]) -> List[datetime]:
    days_top_sender_sent = get_days_top_sender_sent(snaps)

    min_date = min(days_top_sender_sent)
    max_date = max(days_top_sender_sent)

    all_days_sorted = generate_ordered_date_range(min_date, max_date)
    days_top_sender_did_not_send = list(
        set(all_days_sorted) - set(days_top_sender_sent)
    )
    days_top_sender_did_not_send_sorted = sorted(days_top_sender_did_not_send)

    return days_top_sender_did_not_send_sorted


def get_days_top_receiver_did_not_receive(snaps: List[Snap]) -> List[datetime]:
    days_top_receiver_received = get_days_top_receiver_received(snaps)

    min_date = min(days_top_receiver_received)
    max_date = max(days_top_receiver_received)

    all_days_sorted = generate_ordered_date_range(min_date, max_date)
    days_top_receiver_did_not_receive = list(
        set(all_days_sorted) - set(days_top_receiver_received)
    )
    days_top_receiver_did_not_receive_sorted = sorted(days_top_receiver_did_not_receive)

    return days_top_receiver_did_not_receive_sorted


def get_days_top_sender_sent(snaps: List[Snap]) -> List[datetime]:
    top_sender_snaps = filtering.get_by_top_sender(snaps)
    days_top_sender_sent = {snap.timestamp.date() for snap in top_sender_snaps}
    return sorted(list(days_top_sender_sent))


def get_days_top_receiver_received(snaps: List[Snap]) -> List[datetime]:
    top_receiver_snaps = filtering.get_by_top_receiver(snaps)
    days_top_receiver_received = {snap.timestamp.date() for snap in top_receiver_snaps}
    return sorted(list(days_top_receiver_received))

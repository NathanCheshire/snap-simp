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


def get_text_to_media_ratio_by_receiving_user(
    chats: List[Chat], username: str
) -> float:
    """
    Returns the text to media chat ratio of the provided receiving user.

    :param snaps: the list of chats
    :param username: the username to return the text to media chat ratio of from within the provided chats list
    """
    chats_by_username = filtering.get_by_receiving_user(chats, username)
    text_chats, media_chats = filtering.filter_chats_by_type(chats_by_username)
    return len(text_chats) / len(media_chats)


def get_image_to_video_ratio_by_top_sender(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of top sender of snaps from within the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of top sender of snaps from within the provided list
    """

    return get_image_to_video_ratio_by_sending_user(
        snaps, filtering.get_top_sender_username(snaps)
    )


def get_text_to_media_ratio_by_top_sender(chats: List[Chat]) -> float:
    """
    Returns the text to media chat ratio of top sender of chats from within the provided list.

    :param chats: the list of chats
    :return: the text to media chat ratio of top sender of chats from within the provided list
    """

    return get_text_to_media_ratio_by_sending_user(
        chats, filtering.get_top_sender_username(chats)
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


def get_text_to_media_ratio_by_top_receiver(chats: List[Chat]) -> float:
    """
    Returns the text to media chat ratio of top recipient of chats from within the provided list.

    :param chats: the list of chats
    :return: the text to media chat ratio of top recipient of chats from within the provided list
    """

    return get_text_to_media_ratio_by_receiving_user(
        chats, filtering.get_top_receiver_username(chats)
    )


def get_number_by_sender(snaps_or_chats: List[Snap | Chat], username: str):
    """
    Returns the number of snaps or chats the provided user sent.

    :param snaps_or_chats: the list of snaps or chats
    :param username: the username to filter on
    :return: the number of snaps or chats the provided user sent
    """

    return len(filtering.get_by_sending_user(snaps_or_chats, username))


def get_number_by_receiver(snaps_or_chats: List[Snap | Chat], username: str):
    """
    Returns the number of snaps or chats the provided user received.

    :param snaps_or_chats: the list of snaps or chats
    :param username: the username to filter on
    :return: the number of snaps or chats the provided user received
    """

    return len(filtering.get_by_receiving_user(snaps_or_chats, username))


def order_by_time_in_ascending_order(
    snaps_or_chats: List[Snap | Chat],
) -> List[Snap | Chat]:
    """
    Returns the provided snap or chat list after sorting into ascending order by the send time.

    :param snaps_or_chats: the list of snaps or chats to sort into ascending order by send time
    """

    return sorted(snaps_or_chats, key=lambda snap: snap.timestamp)


def order_by_time_in_descending_order(
    snaps_or_chats: List[Snap | Chat],
) -> List[Snap | Chat]:
    """
    Returns the provided snap or chat list after sorting into descending order by the send time.

    :param snaps_or_chats: the list of snaps or chats to sort into descending order by send time
    """

    return sorted(snaps_or_chats, key=lambda snap: snap.timestamp, reverse=True)


def get_date_range(snaps_or_chats: List[Snap | Chat]) -> DateRange:
    """
    Returns the date range of the provided list of snaps or chats meaning the range between which all the snaps or chats fall into.

    :param snaps_or_chats: the list of snaps or chats
    :return: the date range of the snaps or chats of the provided list
    """

    time_ordered = time_ordered = order_by_time_in_ascending_order(snaps_or_chats)
    if len(time_ordered) < 2:
        raise AssertionError("Cannot construct a date range from less than 2 snaps")
    return DateRange(time_ordered[0].timestamp, time_ordered[-1].timestamp)


def get_duration_with_top_sender(snaps_or_chats: List[Snap | Chat]) -> timedelta:
    """
    Returns the duration of the snaps or chats sent by the top sender from within the list.

    :param snaps: the list of snaps or chats
    :return: the duration of snaps or chats with the top sender in the provided list
    """

    top_sender = filtering.get_by_top_sender(snaps_or_chats)
    return get_date_range(top_sender).duration()


def get_duration_with_top_receiver(snaps_or_chats: List[Snap | Chat]) -> timedelta:
    """
    Returns the duration of the snaps or chats received by the top receiver from within the list.

    :param snaps_or_chats: the list of snaps or chats
    :return: the duration of snaps or chats with the top receiver in the provided list
    """

    top_receiver = filtering.get_by_top_receiver(snaps_or_chats)
    return get_date_range(top_receiver).duration()


def get_days_top_sender_did_not_send(
    snaps_or_chats: List[Snap | Chat],
) -> List[datetime]:
    """
    Returns the days from the provided list of which the top sender did not send a snap or chat.

    :param snaps_or_chats: the list of snaps or chats
    :return: the days from the provided list of which the top sender did not send a snap or chat
    """
    days_top_sender_sent = get_days_top_sender_sent(snaps_or_chats)

    min_date = min(days_top_sender_sent)
    max_date = max(days_top_sender_sent)

    all_days_sorted = generate_ordered_date_range(min_date, max_date)
    days_top_sender_did_not_send = list(
        set(all_days_sorted) - set(days_top_sender_sent)
    )
    days_top_sender_did_not_send_sorted = sorted(days_top_sender_did_not_send)

    return days_top_sender_did_not_send_sorted


def get_days_top_receiver_did_not_receive(snaps_or_chats: List[Snap]) -> List[datetime]:
    """
    Returns the days from the provided list of which the top receiver did not receive a snap or chat.

    :param snaps_or_chats: the list of snaps or chats
    :return: the days from the provided list of which the top receiver did not receive a snap or chat
    """
    days_top_receiver_received = get_days_top_receiver_received(snaps_or_chats)

    min_date = min(days_top_receiver_received)
    max_date = max(days_top_receiver_received)

    all_days_sorted = generate_ordered_date_range(min_date, max_date)
    days_top_receiver_did_not_receive = list(
        set(all_days_sorted) - set(days_top_receiver_received)
    )
    days_top_receiver_did_not_receive_sorted = sorted(days_top_receiver_did_not_receive)

    return days_top_receiver_did_not_receive_sorted


def get_days_top_sender_sent(snaps_or_chats: List[Snap | Chat]) -> List[datetime]:
    """
    Returns the days the top sender of the list of snaps or chats sent at least one snap or chat.

    :param snap_or_chats: the list of snaps or chats
    :return: the days the top sender of the list of snaps or chats sent at least one snap or chat
    """
    top_sender_snaps_or_chats = filtering.get_by_top_sender(snaps_or_chats)
    days_top_sender_sent = {snap.timestamp.date() for snap in top_sender_snaps_or_chats}
    return sorted(list(days_top_sender_sent))


def get_days_top_receiver_received(snaps_or_chats: List[Snap | Chat]) -> List[datetime]:
    """
    Returns the days the top receiver of the list of snaps or chats received at least one snap or chat.

    :param snap_or_chats: the list of snaps or chats
    :return: the days the top receiver of the list of snaps or chats received at least one snap or chat
    """
    top_receiver_snaps_or_chats = filtering.get_by_top_receiver(snaps_or_chats)
    days_top_receiver_received = {
        snap.timestamp.date() for snap in top_receiver_snaps_or_chats
    }
    return sorted(list(days_top_receiver_received))

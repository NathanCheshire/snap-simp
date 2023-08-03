from typing import List, Set, Tuple
from snaps.snap import Snap
import snaps.statistics as stats
from snaps.snap_type import SnapType
from chats.chat import Chat
from chats.chat_type import ChatType


def get_by_sending_user(
    snaps_or_chats: List[Snap | Chat], username: str
) -> List[Snap | Chat]:
    """
    Returns all snaps or chats sent by a specific user from the given list.

    :param snaps_or_chats: the list of Snap or Chat objects to analyze
    :param username: the username of the sender
    :return: a list of Snap or Chat objects sent by the specified user
    """

    return [
        snap_or_chat
        for snap_or_chat in snaps_or_chats
        if snap_or_chat.sender == username
    ]


def get_by_receiving_user(
    snaps_or_chats: List[Snap | Chat], username: str
) -> List[Snap | Chat]:
    """
    Returns all snaps or chats received by a specific user from the given list.

    :param snaps_or_chats: the list of Snap or Chat objects to analyze
    :param username: the username of the receiver
    :return: a list of Snap or Chat objects received by the specified user
    """

    return [
        snap_or_chat
        for snap_or_chat in snaps_or_chats
        if snap_or_chat.receiver == username
    ]


def get_top_sender_username(snaps_or_chats: List[Snap | Chat]) -> str:
    """
    Returns the username of the person whos name appears on the most snaps or chats of the provided list.

    :param snaps_or_chats: the list of snaps or chats
    :return: the username of the person who sends/receives the most snaps or chats to/from you
    """

    sorted_sender_username_dict, _ = stats.get_count(snaps_or_chats)
    return next(iter(sorted_sender_username_dict))


def get_top_receiver_username(snaps: List[Snap]) -> str:
    """
    Returns the username of the person whos name appears on the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the username of the person who sends/receives the most snaps to/from you
    """

    _, sorted_receiver_username_dict = stats.get_count(snaps)
    return next(iter(sorted_receiver_username_dict))


def get_by_top_sender(snaps_or_chats: List[Snap | Chat]) -> List[Snap | Chat]:
    """
    Returns a subset of the provided list of snaps or chats containing only the snaps or chats from the top sender

    :param snaps_or_chats: the list of snaps or chats
    :return: a list of snaps containing the snaps or chats from the top sender
    """

    top_sender = get_top_sender_username(snaps_or_chats)
    return get_by_sending_user(snaps_or_chats, top_sender)


def get_by_top_receiver(snaps: List[Snap | Chat]) -> List[Snap | Chat]:
    """
    Returns a subset of the provided list of snaps or chats containing only the snaps or chats to the top receiver

    :param snaps: the list of snaps or chats
    :return: a list of snaps or chats containing the snaps or chats to the top receiver
    """

    top_receiver = get_top_receiver_username(snaps)
    return get_by_receiving_user(snaps, top_receiver)


def filter_snaps_by_type(snaps: List[Snap]) -> Tuple[List[Snap], List[Snap]]:
    """
    Separates a list of Snap objects into two lists: one for images and one for videos.

    :param snaps: A list of Snap objects
    :return: A tuple containing two lists of Snap objects: the first for image snaps and the second for video snaps
    """

    image_snaps = [snap for snap in snaps if snap.type == SnapType.IMAGE]
    video_snaps = [snap for snap in snaps if snap.type == SnapType.VIDEO]

    return image_snaps, video_snaps


def filter_chats_by_type(chats: List[Chat]) -> Tuple[List[Chat], List[Chat]]:
    """
    Separates a list of Chat objects into two lists: one for text and one for media.

    :param chats: A list of Chat objects
    :return: A tuple containing two lists of Chat objects: the first for text chats and the second for media chats
    """

    text_chats = [chat for chat in chats if chat.type == ChatType.TEXT]
    media_chats = [chat for chat in chats if chats.type == ChatType.MEDIA]

    return text_chats, media_chats


def get_unique_sending_usernames(snaps_or_chats: List[Snap | Chat]) -> Set[str]:
    """
    Returns all unique sender usernames from the list of Snap or Chat objects.

    :param snaps: a list of Snap or Chat objects
    :return: a set of unique usernames
    """

    sender_names = {snap_or_chat.sender for snap_or_chat in snaps_or_chats}
    return sender_names


def get_unique_receiving_usernames(snaps_or_chats: List[Snap | Chat]) -> Set[str]:
    """
    Returns all unique receiver usernames from the list of Snap or Chat objects.

    :param snaps_or_chats: a list of Snap or Chat objects
    :return: a set of unique usernames
    """

    receiver_names = {snap_or_chat.receiver for snap_or_chat in snaps_or_chats}
    return receiver_names

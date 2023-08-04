import os
from typing import List
from chats.snapchat_chat_conversation import SnapchatChatConversation
from chats.chat import Chat
from snaps.filtering import (
    get_by_receiving_user,
    get_by_sending_user,
    get_top_receiver_username,
    get_top_sender_username,
)
from snaps.statistics import get_count


def generate_conversation_with(
    their_name: str, sent_chats: List[Chat], received_chats: List[Chat]
) -> SnapchatChatConversation:
    """
    Generates a snapchat chat conversation between you and the provided snapchatter.

    :param their_name: the other snapchatter's username
    :param sent_chats: the list of chats you've sent
    :param received_chats: the list of chats you've received
    :return: a snapchat chat conversation object representing the conversation between you and the other person
    """

    chats_to_them = get_by_receiving_user(sent_chats, their_name)
    chats_from_them = get_by_sending_user(received_chats, their_name)
    all_chats = chats_to_them + chats_from_them

    return SnapchatChatConversation(all_chats)


def generate_conversation_with_top_sender(
    sent_chats: List[Chat],
    received_chats: List[Chat],
) -> SnapchatChatConversation:
    """
    Generates a snapchat chat conversation between you and ther person who sends you the most chats.

    :param sent_chats: the chats you've sent
    :param received_chats: the chats you've received
    :return: a snapchat chat conversation between you and ther person who sends you the most chats
    """

    top_sender = get_top_sender_username(received_chats)
    chats_from_them = get_by_sending_user(received_chats, top_sender)
    chats_to_them = get_by_receiving_user(sent_chats, top_sender)
    all_chats = chats_to_them + chats_from_them

    return SnapchatChatConversation(all_chats)


def generate_conversation_with_top_receiver(
    sent_chats: List[Chat],
    received_chats: List[Chat],
) -> SnapchatChatConversation:
    """
    Generates a snapchat chat conversation between you and ther person who receives the most chats from you.

    :param sent_chats: the chats you've sent
    :param received_chats: the chats you've received
    :return: a snapchat chat conversation between you and ther person who receives the most chats from you
    """

    top_receiver = get_top_receiver_username(sent_chats)
    chats_from_them = get_by_sending_user(received_chats, top_receiver)
    chats_to_them = get_by_receiving_user(sent_chats, top_receiver)
    all_chats = chats_to_them + chats_from_them

    return SnapchatChatConversation(all_chats)


def generate_conversations(
    my_name: str, sent_chats: List[Chat], received_chats: List[Chat]
) -> List[SnapchatChatConversation]:
    """
    Generates all snapchat chat conversations between all unique sender and receiver pairs.

    :param my_name: your snapchat username
    :param sent_chats: the list of chats you've received
    :param received_chats: the list of chats you've recieved
    :return: all snapchat chat conversation objects for all unique sender and receiver pairs
    """

    sender_counts, receiver_counts = get_count(sent_chats + received_chats)
    all_usernames = list(sender_counts.keys()) + list(receiver_counts.keys())
    unique_usernames = list(set(all_usernames))

    ret = []

    for unique_username in unique_usernames:
        if unique_username == my_name:
            continue

        conversation = generate_conversation_with(
            unique_username, sent_chats, received_chats
        )
        ret.append(conversation)

    return ret


def generate_and_save_all_conversations(
    my_name: str,
    sent_chats: List[Chat],
    received_chats: List[Chat],
    save_folder_path: str,
) -> None:
    """
    Generates all snapchat chat conversations between all unique sender and receiver pairs and serializes and saves all objects
    to JSON format to the provided save_folder_path. If this folder does not exist, it will be created.

    :param my_name: your snapchat username
    :param sent_chats: the list of chats you've sent
    :param received_chats: the list of chats you've received
    :param save_folder_path: the location to save all the serialized conversations to
    """

    if not os.path.exists(save_folder_path):
        os.makedirs(save_folder_path)

    conversations = generate_conversations(my_name, sent_chats, received_chats)

    for conversation in conversations:
        their_name = next(
            (
                their_name
                for their_name in conversation.get_users()
                if their_name != my_name
            ),
            None,
        )
        conversation.to_json(os.path.join(save_folder_path, f"{their_name}.json"))

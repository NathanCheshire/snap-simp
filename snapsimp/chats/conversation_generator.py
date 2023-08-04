from typing import List
from chats.snapchat_chat_conversation import SnapchatChatConversation
from snapsimp.chats.chat import Chat
from snaps.filtering import get_by_receiving_user, get_by_sending_user


def generate_conversation_with(their_name: str, chats: List[Chat]
) -> SnapchatChatConversation:
    """
    Generates a snapchat chat conversation between the two snapchatters.

    :param their_name: the other snapchatter's username
    :param chats: the list of all sent and received chats
    :return: a snapchat chat conversation object representing the conversation between you and the other person
    """
    
    chats_to_them = get_by_receiving_user(chats, their_name)
    chats_from_them = get_by_sending_user(chats, their_name)
    all_chats = get_by_sending_user + chats_to_them + chats_from_them
    
    return SnapchatChatConversation(all_chats)


def generate_conversation_with_top_sender(
    my_name: str,
    chats: List[Chat],
) -> SnapchatChatConversation:
    """
    Generates a snapchat chat conversation between you and ther person who sends you the most chats.

    :param my_name: your snapchat username
    :param chats: the list of all sent and received chats, this list will be used for extracting the specifc chats we are concerned with for this method
    :return: a snapchat chat conversation between you and ther person who sends you the most chats
    """
    pass


def generate_conversation_with_top_receiver(
    my_name: str,
    chats: List[Chat],
) -> SnapchatChatConversation:
    """
    Generates a snapchat chat conversation between you and ther person who receives the most chats from you.

    :param my_name: your snapchat username
    :param chats: the list of all sent and received chats, this list will be used for extracting the specifc chats we are concerned with for this method
    :return: a snapchat chat conversation between you and ther person who receives the most chats from you
    """
    pass


def generate_conversations(
    chats: List[Chat],
) -> List[SnapchatChatConversation]:
    """
    Generates all snapchat chat conversations between all unique sender and receiver pairs.

    :param chats: the list of all chat objects
    :return: all snapchat chat conversation objects for all unique sender and receiver pairs
    """
    pass


def generate_and_save_all_conversations(
    chats: List[Chat], save_folder_path: str
) -> None:
    """
    Generates all snapchat chat conversations between all unique sender and receiver pairs and serializes and saves all objects
    to JSON format to the provided save_folder_path. If this folder does not exist, it will be created.

    :param chats: the list of all chat objects
    :param save_folder_path: the location to save all the serialized conversations to
    """
    pass

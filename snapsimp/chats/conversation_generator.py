from typing import List
from snaps.snapchat_snap_conversation import SnapchatSnapConversation
from snapsimp.chats.chat import Chat


def generate_conversation_with(
    my_name: str, their_name: str
) -> SnapchatSnapConversation:
    pass


def generate_conversation_with_top_sender(
    chats: List[Chat],
) -> SnapchatSnapConversation:
    pass


def generate_conversation_with_top_receiver(
    chats: List[Chat],
) -> SnapchatSnapConversation:
    pass


def generate_conversations(
    chats: List[Chat],
) -> List[SnapchatSnapConversation]:
    pass


def generate_and_save_all_conversations(
    chats: List[Chat],
) -> List[SnapchatSnapConversation]:
    pass

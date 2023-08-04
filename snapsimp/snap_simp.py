import argparse
import json
from snaps.snapchat_snap_conversation import SnapchatSnapConversation
from chats.snapchat_chat_conversation import SnapchatChatConversation
from chats.chat_type import ChatType
from soup.snap_history_parsing import extract_snap_history
from soup.account_parsing import parse_all
from soup.chat_history_parsing import extract_chat_history
from snaps.filtering import (
    get_by_top_receiver,
    get_by_top_sender,
    filter_snaps_by_type,
)
from chats.conversation_generator import generate_conversation_with_top_receiver

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A parser for Snapchat data exports")
    parser.add_argument(
        "-shf",
        "--snap-history-file",
        help="The path to the Snapchat snap history HTML file",
        default="html/snap_history.html",
    )
    parser.add_argument(
        "-chf",
        "--chat-history-file",
        help="The path to the Snapchat chat history HTML file",
        default="html/chat_history.html",
    )
    parser.add_argument(
        "-af",
        "--account-file",
        help="The path to the Snapchat account HTML file",
        default="html/account.html",
    )
    args = parser.parse_args()

    basic_user_info, device_information, device_history, login_history = parse_all(
        args.account_file
    )

    received_snaps, sent_snaps = extract_snap_history(
        args.snap_history_file, basic_user_info.username
    )
    received_chats, sent_chats = extract_chat_history(
        args.chat_history_file, basic_user_info.username
    )
    all_chats = received_chats + sent_chats

    our_conversation = generate_conversation_with_top_receiver(sent_chats, received_chats)
    our_conversation.to_json("Her.json")
    # generate_and_save_all_conversations(all_chats, "all-chat-conversations")

    print("End Program")

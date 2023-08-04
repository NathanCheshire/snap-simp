import argparse
from soup.snap_history_parsing import extract_snap_history
from soup.account_parsing import parse_all
from soup.chat_history_parsing import extract_chat_history
from chats.conversation_generator import generate_and_save_all_conversations

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
    all_snaps = received_snaps + sent_snaps

    received_chats, sent_chats = extract_chat_history(
        args.chat_history_file, basic_user_info.username
    )
    all_chats = received_chats + sent_chats

    our_conversation = generate_and_save_all_conversations(
        basic_user_info.username, sent_chats, received_chats, "all-chat-conversations"
    )

    print("End Program")

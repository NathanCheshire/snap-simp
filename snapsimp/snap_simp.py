import argparse
from snaps.snapchat_snap_conversation import SnapchatSnapConversation
from soup.snap_history_parsing import extract_snap_history
from soup.account_parsing import parse_all
from soup.chat_history_parsing import extract_chat_history
from snaps.filtering import (
    get_snaps_by_top_receiver,
    get_snaps_by_top_sender,
    filter_snaps_by_type,
)
from snaps.statistics import (
    get_days_top_sender_sent,
    get_days_top_sender_did_not_send,
    get_days_top_receiver_did_not_receive,
    get_days_top_receiver_received,
)

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

    top_sender_to_me_snaps = get_snaps_by_top_sender(received_snaps)
    top_receiver_from_me_snaps = get_snaps_by_top_receiver(sent_snaps)

    sent_snaps, sent_videos = filter_snaps_by_type(top_receiver_from_me_snaps)
    received_snaps, received_videos = filter_snaps_by_type(top_sender_to_me_snaps)

    days_she_sent = get_days_top_sender_sent(received_snaps)
    days_she_did_not_send = get_days_top_sender_did_not_send(received_snaps)

    days_i_sent = get_days_top_receiver_received(sent_snaps)
    days_i_did_not_send = get_days_top_receiver_did_not_receive(sent_snaps)

    our_snaps = top_sender_to_me_snaps + top_receiver_from_me_snaps
    our_conversation = SnapchatSnapConversation(our_snaps)

    received_chats, sent_chats = extract_chat_history(
        args.chat_history_file, basic_user_info.username
    )

    for received_chat in received_chats:
        print(received_chat)

    print("Fireworks when we're together, thunderclouds when we're apart")

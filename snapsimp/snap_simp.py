import argparse
from snaps.snapchat_snap_conversation import SnapchatSnapConversation
from soup.snap_history_parsing import extract_snap_history
from soup.account_parsing import parse_basic_user_info, parse_device_information, parse_device_history
from snaps.filtering import get_snaps_by_top_receiver, get_snaps_by_top_sender, filter_snaps_by_type
from snaps.statistics import get_days_top_sender_sent, get_days_top_sender_did_not_send, get_days_top_receiver_did_not_receive, get_days_top_receiver_received

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('-sh', '--snap-history-file', help='The path to the Snapchat snap history HTML file', default='html/snap_history.html')
    parser.add_argument('-acc', '--account-file', help='The path to the Snapchat account HTML file', default='html/account.html')
    args = parser.parse_args()

    basic_user_info = parse_basic_user_info(args.account_file)
    device_information = parse_device_information(args.account_file)
    device_history = parse_device_history(args.account_file)
    print(device_history)

    received, sent = extract_snap_history(args.snap_history_file, basic_user_info.username) 

    top_sender_to_me_snaps = get_snaps_by_top_sender(received)
    top_receiver_from_me_snaps = get_snaps_by_top_receiver(sent)

    sent_snaps, sent_videos = filter_snaps_by_type(top_receiver_from_me_snaps)
    received_snaps, received_videos = filter_snaps_by_type(top_sender_to_me_snaps)

    days_she_sent = get_days_top_sender_sent(received)
    days_she_did_not_send = get_days_top_sender_did_not_send(received)

    days_i_sent = get_days_top_receiver_received(sent)
    days_i_did_not_send = get_days_top_receiver_did_not_receive(sent)

    our_snaps = top_sender_to_me_snaps + top_receiver_from_me_snaps
    conversation = SnapchatSnapConversation(our_snaps)

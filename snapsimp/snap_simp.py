import argparse
from selenium.selenium_utils import extract_snap_history, parse_basic_user_info_from_account_html
from snaps.filtering import get_snaps_by_top_receiver, get_snaps_by_top_sender, filter_snaps_by_type
from snaps.statistics import get_days_top_sender_sent, get_days_top_sender_did_not_send

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('-sh', '--snap-history-file', help='The path to the Snapchat snap history HTML file', default='html/snap_history.html')
    parser.add_argument('-acc', '--account-file', help='The path to the Snapchat account HTML file', default='html/account.html')
    args = parser.parse_args()

    basic_user_info = parse_basic_user_info_from_account_html(args.account_file)
    received, sent = extract_snap_history(args.snap_history_file, basic_user_info.username) 

    top_sender_to_me_snaps = get_snaps_by_top_sender(received)
    top_receiver_from_me_snaps = get_snaps_by_top_receiver(sent)

    sent_snaps, sent_videos = filter_snaps_by_type(top_receiver_from_me_snaps)
    received_snaps, received_videos = filter_snaps_by_type(top_sender_to_me_snaps)

    days_she_sent = get_days_top_sender_sent(received)
    days_she_did_not_send = get_days_top_sender_did_not_send(received)

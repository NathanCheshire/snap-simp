import argparse
from selenium.selenium_utils import extract_snap_history, parse_basic_user_info_from_account_html
from snaps.filtering import filter_snaps_by_type, get_snaps_by_top_username, get_top_username
from snaps.statistics import calculate_min_avg_max_time_between_snaps_of_top_user


if __name__ == '__main__':
    # todo we need to allow multiple files to be passed in but default to the default names assuming they are in html/
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('snap_history_file', help='The path to the Snapchat snap history HTML file', required=False, default='html/snap_history.html')
    parser.add_argument('account_file', help='The path to the Snapchat account HTML file', required=False, default='html/account.html')

    args = parser.parse_args()

    basic_user_info = parse_basic_user_info_from_account_html(args.account_file)
    print(extract_snap_history(args.snap_history_file, basic_user_info.username))
    
    # received, sent = extract_snap_history(args.file) 
    # top_sender_snaps = get_snaps_by_top_username(received)
    # image_snaps, video_snaps = filter_snaps_by_type(top_sender_snaps)
   
    # print(calculate_min_avg_max_time_between_snaps_of_top_user(sent, received))

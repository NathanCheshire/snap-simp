import argparse
from selenium.selenium_utils import extract_snap_history, parse_basic_user_info_from_account_html
from snaps.filtering import filter_snaps_by_type, get_snaps_by_top_username, get_top_username
from snaps.statistics import calculate_min_avg_max_time_between_snaps_of_top_user


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('file', help='The path to the Snapchat snap history HTML file')

    args = parser.parse_args()

    print(parse_basic_user_info_from_account_html(args.file))
    
    # received, sent = extract_snap_history(args.file) 
    # top_sender_snaps = get_snaps_by_top_username(received)
    # image_snaps, video_snaps = filter_snaps_by_type(top_sender_snaps)
   
    # print(calculate_min_avg_max_time_between_snaps_of_top_user(sent, received))

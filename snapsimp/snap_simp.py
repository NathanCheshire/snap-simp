import argparse
from selenium.selenium_utils import extract_snap_history
from snaps.filtering import filter_snaps_by_type, get_snaps_by_top_username
from snaps.statistics import get_image_to_video_ratio_by_top_username
from snaps.statistics import calculate_avg_time_between_top_snapper


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('file', help='The path to the Snapchat snap history HTML file')

    args = parser.parse_args()
    
    received, sent = extract_snap_history(args.file) 
    top_sender_snaps = get_snaps_by_top_username(received)
    image_snaps, video_snaps = filter_snaps_by_type(top_sender_snaps)
   
    print(calculate_avg_time_between_top_snapper(sent, received))

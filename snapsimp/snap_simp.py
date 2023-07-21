import argparse
from selenium.utils import extract_snap_history
from snaps.filtering import filter_snaps_by_type, get_snaps_by_top_username
from snaps.visualization_helpers import get_image_to_video_ratio_by_top_username


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('file', help='The path to the Snapchat snap history HTML file')

    args = parser.parse_args()
    
    received, sent = extract_snap_history(args.file) 
    top_sender_snaps = get_snaps_by_top_username(received)
    image_snaps, video_snaps = filter_snaps_by_type(top_sender_snaps)
   
    print(get_image_to_video_ratio_by_top_username(received))

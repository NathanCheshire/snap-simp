import argparse
from selenium.selenium_utils import extract_snap_history, parse_basic_user_info_from_account_html


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('-sh', '--snap-history-file', help='The path to the Snapchat snap history HTML file', default='html/snap_history.html')
    parser.add_argument('-acc', '--account-file', help='The path to the Snapchat account HTML file', default='html/account.html')
    args = parser.parse_args()

    basic_user_info = parse_basic_user_info_from_account_html(args.account_file)
    received, sent = extract_snap_history(args.snap_history_file, basic_user_info.username) 
    print('hello world')

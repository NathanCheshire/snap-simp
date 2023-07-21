import argparse
from typing import Dict, List, Set, Tuple
from bs4 import BeautifulSoup
from collections import Counter
from snap import Snap, SnapType

# The number of columns the Snap History Metadata html page includes.
SNAP_HISTORY_NUM_TABLE_COLUMNS = 3

# The amount of tables the HTML document should contain.
NUM_TABLES = 2
RECEIVED_SNAPS_TABLE_INDEX = 0
SENT_SNAPS_TABLE_INDEX = 1

SENDER_COLUMN_INDEX = 0
TYPE_COLUMN_INDEX = 1
TIMESTAMP_COLUMN_INDEX = 2

# Tags for document traversal, todo enum?
BODY = 'body'
TABLE = 'table'
TABLE_ROW = 'tr'
TABLE_DATA_CELL = 'td'

def parse_snap_history_table(table: BeautifulSoup) -> List[Snap]:
    """
    
    """
    snaps = []
    if not table:
        return snaps

    rows = table.find_all(TABLE_ROW)

    for row in rows:
        columns = row.find_all(TABLE_DATA_CELL)

        if len(columns) < SNAP_HISTORY_NUM_TABLE_COLUMNS:
            continue

        sender = columns[SENDER_COLUMN_INDEX].get_text()
        snap_type = SnapType.IMAGE if columns[TYPE_COLUMN_INDEX].get_text() == 'IMAGE' else SnapType.VIDEO
        timestamp = columns[TIMESTAMP_COLUMN_INDEX].get_text()
        snaps.append(Snap(sender, snap_type, timestamp))

    return snaps


def extract_snap_history(filename: str) -> Tuple[List[Snap], List[Snap]]:
    """
    Extracts the snap history, both sent and received snaps, from the provided snap history html file.
    This file is expected to have two and only two tables, the first should be the received snaps table
    and the second should be the sent snaps table.

    :param filename: the path to the local html file
    :returns: two lists of snap objects, the first is the received snaps, the second is the sent snaps
    """

    with open(filename, 'r') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')

    tables = soup.find_all(TABLE)

    if len(tables) != NUM_TABLES: 
        print(f"Error: A table amount not equal to {NUM_TABLES} tables found in {filename}; num tables: {len(tables)}")
        return [], []

    received_snaps = parse_snap_history_table(tables[RECEIVED_SNAPS_TABLE_INDEX])
    sent_snaps = parse_snap_history_table(tables[SENT_SNAPS_TABLE_INDEX])

    return received_snaps, sent_snaps



def compute_sender_frequency(snaps: List[Snap]) -> Dict[str, int]:
    """
    Computes and returns a dictionary detailing the frequency of a particular sender/receiver.

    Example returned schema:
    {
        "mybestfriend": 143,
        "mysister": 22,
        "mycousin": 15
    }

    :param snaps: the list of snaps to compute the sender frequency of
    :return: a dictionary detailing the frequency of a particular sender/receiver
    """

    username_counter = Counter(snap.sender for snap in snaps)
    sorted_username_counts = sorted(username_counter.items(), key=lambda item: item[1], reverse=True)
    sorted_username_dict = dict(sorted_username_counts)
    return sorted_username_dict

def get_unique_usernames(snaps: List[Snap]) -> Set[str]:
    """
    Returns all unique usernames from a list of Snap objects.

    :param snaps: A list of Snap objects
    :return: A set of unique usernames.
    """

    unique_usernames = {snap.sender for snap in snaps}
    return unique_usernames

def get_snap_type_frequency(snaps: List[Snap]) -> Dict[SnapType, int]:
    """
    Count the number of each type of snap in the given list.

    :param snaps: The list of Snap objects to analyze
    :return: A dictionary mapping each snap type to its frequency
    """

    type_counts = Counter([snap.type for snap in snaps])
    return type_counts

def get_snaps_by_user(snaps: List[Snap], username: str) -> List[Snap]:
    """
    Returns all snaps sent by a specific user from the given list.

    :param snaps: The list of Snap objects to analyze
    :param username: The username of the sender
    :return: A list of Snap objects sent by the specified user
    """
    return [snap for snap in snaps if snap.sender == username]

def get_top_username(snaps: List[Snap]) -> str:
    """
    Returns the username of the person whos name appears on the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the username of the person whos name appears on the most snaps
    """

    frequency = compute_sender_frequency(snaps)
    return next(iter(frequency))

def get_snaps_by_top_username(snaps: List[Snap]) -> List[Snap]:
    """
    Returns a subset of the provided list of snaps containing only the snaps to/from the highest receiver/sender.

    :param snaps: the list of snaps
    :return: a list of snaps containing the snaps to/from the top receiver/sender. If the provided list was snaps
    received by you, the subset would contain the snaps sent from the person who snaps you the most. If the provided
    list was snaps sent by you, the subset would contain the snaps received from the person who you snap the most.
    """
    top_user = get_top_username(snaps)
    return get_snaps_by_user(snaps, top_user)

def filter_snaps_by_type(snaps: List[Snap]) -> Tuple[List[Snap], List[Snap]]:
    """
    Separates a list of Snap objects into two lists: one for images and one for videos.

    :param snaps: A list of Snap objects
    :return: A tuple containing two lists of Snap objects: the first for image snaps and the second for video snaps
    """
    image_snaps = [snap for snap in snaps if snap.type == SnapType.IMAGE]
    video_snaps = [snap for snap in snaps if snap.type == SnapType.VIDEO]

    return image_snaps, video_snaps

def get_image_to_video_ratio_by_username(snaps: List[Snap], username: str) -> float:
    """
    Returne the image to video snap ratio of the provided username.

    :param snaps: the list of snaps
    :param username: the username to return the image to video snap ratio of from within the provided snaps list.
    """

    snaps_from_user = get_snaps_by_user(snaps, username)
    image_snaps, video_snaps = filter_snaps_by_type(snaps_from_user)
    return len(image_snaps) / len(video_snaps)

def get_image_to_video_ratio_by_top_username(snaps: List[Snap]) -> float:
    """
    Returns the image to video snap ratio of the user with the most snaps of the provided list.

    :param snaps: the list of snaps
    :return: the image to video snap ratio of the user with the most snaps in the list. For example,
    if this was the snaps you received, this would return the ratio of image to video snaps of the person
    who sent you the most snaps
    """

    return get_image_to_video_ratio_by_username(snaps, get_top_username(snaps))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('file', help='The path to the Snapchat snap history HTML file')

    args = parser.parse_args()
    
    received, sent = extract_snap_history(args.file) 
    top_sender_snaps = get_snaps_by_top_username(received)
    image_snaps, video_snaps = filter_snaps_by_type(top_sender_snaps)
   
    print(get_image_to_video_ratio_by_top_username(received))

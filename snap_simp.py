import argparse
from typing import Dict, List, Set, Tuple
from bs4 import BeautifulSoup
from collections import Counter
from snap import Snap, SnapType

# The number of columns the Snap History Metadata html page includes
SNAP_HISTORY_NUM_TABLE_COLUMNS = 3
MIN_TABLES = 2
RECEIVED_SNAPS_TABLE_INDEX = 0
SENT_SNAPS_TABLE_INDEX = 1

# Tags for document traversal
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

        sender = columns[0].get_text()
        snap_type = SnapType.IMAGE if columns[1].get_text() == 'IMAGE' else SnapType.VIDEO
        timestamp = columns[2].get_text()
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

    if len(tables) < MIN_TABLES: 
        print(f"Error: Less than {MIN_TABLES} tables found in {filename}")
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

    :param snaps: A list of Snap objects.
    :return: A set of unique usernames.
    """

    unique_usernames = {snap.sender for snap in snaps}
    return unique_usernames

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A parser for Snapchat data exports')
    parser.add_argument('file', help='The path to the Snapchat snap history HTML file')

    args = parser.parse_args()

    # todo argparse this but default to this
    received, sent = extract_snap_history(args.file) 
    print(compute_sender_frequency(received))
    print(compute_sender_frequency(sent))

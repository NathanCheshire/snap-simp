from typing import  List, Tuple
from bs4 import BeautifulSoup
from snapsimp.snaps.snap import Snap, SnapType
from snapsimp.selenium.table_elements import TableElements

# The number of columns the Snap History Metadata html page includes.
SNAP_HISTORY_NUM_TABLE_COLUMNS = 3

# The amount of tables the HTML document should contain.
NUM_TABLES = 2
RECEIVED_SNAPS_TABLE_INDEX = 0
SENT_SNAPS_TABLE_INDEX = 1

SENDER_COLUMN_INDEX = 0
TYPE_COLUMN_INDEX = 1
TIMESTAMP_COLUMN_INDEX = 2

def parse_snap_history_table(table: BeautifulSoup) -> List[Snap]:
    """
    
    """
    snaps = []
    if not table:
        return snaps

    rows = table.find_all(TableElements.TABLE_ROW.value)

    for row in rows:
        columns = row.find_all(TableElements.TABLE_DATA_CELL.value)

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

    tables = soup.find_all(TableElements.TABLE.value)

    if len(tables) != NUM_TABLES: 
        print(f"Error: A table amount not equal to {NUM_TABLES} tables found in {filename}; num tables: {len(tables)}")
        return [], []

    received_snaps = parse_snap_history_table(tables[RECEIVED_SNAPS_TABLE_INDEX])
    sent_snaps = parse_snap_history_table(tables[SENT_SNAPS_TABLE_INDEX])

    return received_snaps, sent_snaps
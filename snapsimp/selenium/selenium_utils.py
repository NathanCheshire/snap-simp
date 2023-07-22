from typing import  List, Tuple
from bs4 import BeautifulSoup
from snaps.snap import Snap
from selenium.table_elements import TableElements
from snaps.snap_type import SnapType
from snaps.snap_direction import SnapDirection
from common.basic_user_info import BasicUserInfo
from selenium.html_headers import HtmlHeaders


# Constants for the snap_history.html file.
SNAP_HISTORY_NUM_TABLE_COLUMNS = 3
SNAP_HISTORY_NUM_TABLES = 2
RECEIVED_SNAPS_TABLE_INDEX = 0
SENT_SNAPS_TABLE_INDEX = 1
SENDER_COLUMN_INDEX = 0
TYPE_COLUMN_INDEX = 1
TIMESTAMP_COLUMN_INDEX = 2


# Constants for the account.html file.
ACCOUNT_HTML_HEADERS = ["Basic Information", "Device Information", "Device History", "Login History"]


def parse_basic_user_info_from_account_html(filename: str) -> BasicUserInfo:
    """
    Extracts the basic information from the account.html file.

    :param filename: the path to the html file containing the account data
    :return: a BasicUserInfo object
    """

    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    headers = soup.find_all(HtmlHeaders.H3.value)

    if len(headers) != len(ACCOUNT_HTML_HEADERS):
        raise ValueError(f"Unexpected number of {HtmlHeaders.H3.value} headers. Expected {len(ACCOUNT_HTML_HEADERS)}, found {len(headers)}")

    for i in range(len(ACCOUNT_HTML_HEADERS)):
        if headers[i].text != ACCOUNT_HTML_HEADERS[i]:
            raise ValueError(f"Unexpected {HtmlHeaders.H3.value} header at position {i}. Expected '{ACCOUNT_HTML_HEADERS[i]}', found '{headers[i].text}'")

    table = soup.find(TableElements.TABLE.value)
    rows = table.find_all(TableElements.TABLE_ROW.value)

    username_row = rows[0]
    name_row = rows[1]
    creation_date_row = rows[2]

    username = username_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()
    name = name_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()
    creation_date = creation_date_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()

    return BasicUserInfo(username, name, creation_date)


def parse_snap_history_table(table: BeautifulSoup, snap_direction: SnapDirection) -> List[Snap]:
    """
    Parses a nspa history table using the provided table. All snaps are tagged with the provided direction.

    :param table: the HTML extracted table element
    :param snap_direction: the direction of this snap table such as received or sent
    :return: a list of Snap objects
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
        snaps.append(Snap(sender, snap_type, timestamp, snap_direction))

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

    if len(tables) != SNAP_HISTORY_NUM_TABLES: 
        print(f"Error: A table amount not equal to {SNAP_HISTORY_NUM_TABLES} tables found in {filename}; num tables: {len(tables)}")
        return [], []

    received_snaps = parse_snap_history_table(tables[RECEIVED_SNAPS_TABLE_INDEX], SnapDirection.RECEIVED)
    sent_snaps = parse_snap_history_table(tables[SENT_SNAPS_TABLE_INDEX], SnapDirection.SENT)

    return received_snaps, sent_snaps
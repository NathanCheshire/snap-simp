from typing import List, Tuple
from bs4 import BeautifulSoup
from snaps.snap import Snap
from snaps.snap_history_table_column_indicie import SnapHistoryTableColumnIndicie
from common.snap_simp_enum import SnapSimpEnum
from soup.table_elements import TableElements
from snaps.snap_type import SnapType


class __SnapDirection(SnapSimpEnum):
    RECEIVED = 0
    SENT = 1

    def __init__(self, table_index):
        self.table_index = table_index
        self.name_str = self.name


def __parse_snap_history_table(
    table: BeautifulSoup, snap_direction: __SnapDirection, my_name: str
) -> List[Snap]:
    """
    Parses a nspa history table using the provided table. All snaps are tagged with the provided direction.

    :param table: the HTML extracted table element
    :param snap_direction: the direction of this snap table such as received or sent
    :param my_name: your snapchat account username
    :return: a list of Snap objects
    """

    snaps = []

    if not table:
        return snaps

    rows = table.find_all(TableElements.TABLE_ROW.value)

    for row in rows:
        columns = row.find_all(TableElements.TABLE_DATA_CELL.value)

        if len(columns) != len(SnapHistoryTableColumnIndicie.values()):
            continue

        other_account_username = columns[
            SnapHistoryTableColumnIndicie.SENDER.value
        ].get_text()
        snap_type = (
            SnapType.IMAGE
            if columns[SnapHistoryTableColumnIndicie.TYPE.value].get_text()
            == SnapType.IMAGE.value
            else SnapType.VIDEO
        )
        timestamp = columns[SnapHistoryTableColumnIndicie.TIME_STAMP.value].get_text()

        sender = __get_sender(snap_direction, my_name, other_account_username)
        receiver = __get_receiver(snap_direction, my_name, other_account_username)

        snaps.append(Snap(sender, receiver, snap_type, timestamp))

    return snaps


def __get_sender(snap_direction: __SnapDirection, my_name: str, other_name: str) -> str:
    """
    Returns the person who sent a snap based on the direction.

    :param snap_direction: the snap direction i.e. whether we received or sent the snap
    :param my_name: your account username
    :param other_name: the other person's account username
    """
    return other_name if snap_direction == __SnapDirection.RECEIVED else my_name


def __get_receiver(
    snap_direction: __SnapDirection, my_name: str, other_name: str
) -> str:
    """
    Returns the person who received a snap based on the direction.

    :param snap_direction: the snap direction i.e. whether we received or sent the snap
    :param my_name: your account username
    :param other_name: the other person's account username
    """
    return my_name if snap_direction == __SnapDirection.RECEIVED else other_name


def extract_snap_history(
    snap_history_file_name: str, my_name: str
) -> Tuple[List[Snap], List[Snap]]:
    """
    Extracts the snap history, both sent and received snaps, from the provided snap history html file.
    This file is expected to have two and only two tables, the first should be the received snaps table
    and the second should be the sent snaps table.

    :param snap_history_file_name: the path to the local snap_history.html file
    :param my_name: your snapchat account username, for me this is nathanvcheshire
    :returns: two lists of snap objects, the first is the received snaps, the second is the sent snaps
    """

    with open(snap_history_file_name, "r") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    tables = soup.find_all(TableElements.TABLE.value)

    if len(tables) != len(__SnapDirection.values()):
        raise AssertionError(
            f"Error: A table amount not equal to {len(__SnapDirection.values())} tables found in {snap_history_file_name}; num tables: {len(tables)}"
        )

    received_snaps = __parse_snap_history_table(
        tables[__SnapDirection.RECEIVED.table_index], __SnapDirection.RECEIVED, my_name
    )
    sent_snaps = __parse_snap_history_table(
        tables[__SnapDirection.SENT.table_index], __SnapDirection.SENT, my_name
    )

    return received_snaps, sent_snaps

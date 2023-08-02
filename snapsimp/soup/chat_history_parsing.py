from typing import List, Tuple
from bs4 import BeautifulSoup
from common.snap_simp_enum import SnapSimpEnum
from chats.chat import Chat
from chats.chat_type import ChatType
from chats.chat_history_table_column_indicie import ChatHistoryTableColumnIndicie
from soup.table_elements import TableElements


class __ChatDirection(SnapSimpEnum):
    RECEIVED = 0
    SENT = 1

    def __init__(self, table_index):
        self.table_index = table_index
        self.name_str = self.name


def __parse_chat_history_table(
    table: BeautifulSoup, chat_direction: __ChatDirection, my_name: str
) -> List[Chat]:
    """
    Parses a chat history table using the provided table. All chats are tagged with the provided direction.

    :param table: the HTML extracted table element
    :param chat_direction: the direction of this chat table such as received or sent
    :param my_name: your snapchat account username
    :return: a list of Chat objects
    """

    chats = []

    if not table:
        return chats

    rows = table.find_all(TableElements.TABLE_ROW.value)

    for row in rows:
        columns = row.find_all(TableElements.TABLE_DATA_CELL.value)

        if len(columns) != len(ChatHistoryTableColumnIndicie.values()):
            continue

        other_account_username = columns[
            ChatHistoryTableColumnIndicie.SENDER.value
        ].get_text()
        chat_type = (
            ChatType.IMAGE
            if columns[ChatHistoryTableColumnIndicie.TYPE.value].get_text()
            == ChatType.IMAGE.value
            else ChatType.VIDEO
        )
        timestamp = columns[ChatHistoryTableColumnIndicie.TIME_STAMP.value].get_text()

        sender = __get_sender(chat_direction, my_name, other_account_username)
        receiver = __get_receiver(chat_direction, my_name, other_account_username)

        chats.append(Chat(sender, receiver, chat_type, timestamp))

    return chats


def __get_sender(chat_direction: __ChatDirection, my_name: str, other_name: str) -> str:
    """
    Returns the person who sent a chat based on the direction.

    :param chat_direction: the chat direction i.e. whether we received or sent the chat
    :param my_name: your account username
    :param other_name: the other person's account username
    """
    return other_name if chat_direction == __ChatDirection.RECEIVED else my_name


def __get_receiver(
    chat_direction: __ChatDirection, my_name: str, other_name: str
) -> str:
    """
    Returns the person who received a chat based on the direction.

    :param chat_direction: the chat direction i.e. whether we received or chat the chat
    :param my_name: your account username
    :param other_name: the other person's account username
    """
    return my_name if chat_direction == __ChatDirection.RECEIVED else other_name


def extract_chat_history(
    chat_history_file_name: str, my_name: str
) -> Tuple[List[Chat], List[Chat]]:
    """
    Extracts the chat history, both sent and received chats, from the provided chat history html file.
    This file is expected to have two and only two tables, the first should be the received chats table
    and the second should be the sent chats table.

    :param chat_history_file_name: the path to the local chat_history.html file
    :param my_name: your snapchat account username, for me this is nathanvcheshire
    :returns: two lists of chat objects, the first is the received chats, the second is the sent chats
    """

    with open(chat_history_file_name, "r") as file:
        soup = BeautifulSoup(file.read(), "html.parser")

    tables = soup.find_all(TableElements.TABLE.value)

    if len(tables) != len(__ChatDirection.values()):
        raise AssertionError(
            f"Error: A table amount not equal to {len(__ChatDirection.values())} tables found in {chat_history_file_name}; num tables: {len(tables)}"
        )

    received_chats = __parse_chat_history_table(
        tables[__ChatDirection.RECEIVED.table_index], __ChatDirection.RECEIVED, my_name
    )
    sent_chats = __parse_chat_history_table(
        tables[__ChatDirection.SENT.table_index], __ChatDirection.SENT, my_name
    )

    return received_chats, sent_chats

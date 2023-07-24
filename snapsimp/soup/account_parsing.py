from typing import List
from common.basic_user_info import BasicUserInfo
from common.device_info import DeviceInformation
from common.device_history import DeviceHistory
from common.login_history import LoginHistory
from soup.html_headers import HtmlHeaders
from soup.table_elements import TableElements
from bs4 import BeautifulSoup


HTML_HEADERS = ["Basic Information", "Device Information", "Device History", "Login History"]


def parse_basic_user_info(filename: str) -> BasicUserInfo:
    """
    Extracts the basic information from a standard account.html file.

    :param filename: the path to the html file containing the account data
    :return: a BasicUserInfo object
    """

    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    headers = soup.find_all(HtmlHeaders.H3.value)

    if len(headers) != len(HTML_HEADERS):
        raise ValueError(f"Unexpected number of {HtmlHeaders.H3.value} headers. Expected {len(HTML_HEADERS)}, found {len(headers)}")

    for i in range(len(HTML_HEADERS)):
        if headers[i].text != HTML_HEADERS[i]:
            raise ValueError(f"Unexpected {HtmlHeaders.H3.value} header at position {i}. Expected '{HTML_HEADERS[i]}', found '{headers[i].text}'")

    table = soup.find(TableElements.TABLE.value)
    rows = table.find_all(TableElements.TABLE_ROW.value)

    username_row = rows[0]
    name_row = rows[1]
    creation_date_row = rows[2]

    username = username_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()
    name = name_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()
    creation_date = creation_date_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()

    return BasicUserInfo(username, name, creation_date)

def parse_device_information(filename: str) -> DeviceInformation:
    """
    Extracts the device information from a standard account.html file.

    :param filename: the path to the html file containing the device information data
    :return: a DeviceInformation object
    """
    pass

def parse_device_history(filename: str) -> List[DeviceHistory]:
    """
    Extracts the device history from a standard account.html file.

    :param filename: the path to the html file containing the device history data
    :return: a DeviceHistory object
    """
    pass

def parse_login_history(filename: str) -> List[LoginHistory]:
    """
    Extracts the login history from a standard account.html file.

    :param filename: the path to the html file containing the login history data
    :return: a LoginHistory object
    """
    pass
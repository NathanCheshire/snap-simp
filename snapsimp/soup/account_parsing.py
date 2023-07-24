from datetime import datetime
from enum import Enum
import re
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
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    headers = soup.find_all(HtmlHeaders.H3.value)

    if len(headers) != len(HTML_HEADERS):
        raise ValueError(f"Unexpected number of {HtmlHeaders.H3.value} headers. Expected {len(HTML_HEADERS)}, found {len(headers)}")

    for i in range(len(HTML_HEADERS)):
        if headers[i].text != HTML_HEADERS[i]:
            raise ValueError(f"Unexpected {HtmlHeaders.H3.value} header at position {i}. Expected '{HTML_HEADERS[i]}', found '{headers[i].text}'")

    tables = soup.find_all(TableElements.TABLE.value)
    device_information_table = tables[1]

    rows = device_information_table.find_all(TableElements.TABLE_ROW.value)
    make_row = rows[0]
    model_row = rows[1]
    model_name_row = rows[2]
    user_agent_row = rows[3]
    language_row = rows[4]
    os_type_row = rows[5]
    os_version_row = rows[6]
    connection_type_row = rows[7]

    make = make_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    model_id = model_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    model_name = model_name_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    user_agent = user_agent_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    language = language_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    os_type = os_type_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    os_version = os_version_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    connection_type = [type.strip() for type in connection_type_row.find_all(TableElements.TABLE_HEADER.value)[1].text.split(',')]

    return DeviceInformation(make, model_id, model_name, user_agent, language, os_type, os_version, connection_type)

class DeviceLabels(Enum):
    MAKE = "Make:"
    MODEL = "Model:"
    START_TIME = "Start Time:"
    DEVICE_TYPE = "Device Type:"   

def __parse_device_history_html(row) -> DeviceHistory:
    """
    Extracts the device history from a BeautifulSoup row object.

    :param row: BeautifulSoup object representing a table row containing the device history data
    :return: a DeviceHistory object
    """
    row_str = re.sub("<.*?>", "", str(row))
    labels = [DeviceLabels.MAKE.value, DeviceLabels.MODEL.value, DeviceLabels.START_TIME.value, DeviceLabels.DEVICE_TYPE.value]
    device_info = {}

    for i in range(len(labels)-1):
        start = row_str.find(labels[i]) + len(labels[i])
        end = row_str.find(labels[i+1])
        device_info[labels[i]] = row_str[start:end].strip()

    device_info[labels[-1]] = row_str[row_str.find(labels[-1]) + len(labels[-1]):].strip()

    return DeviceHistory(make=device_info[DeviceLabels.MAKE.value],
                         model=device_info[DeviceLabels.MODEL.value],
                         start_time=device_info[DeviceLabels.START_TIME.value],
                         device_type=device_info[DeviceLabels.DEVICE_TYPE.value])

def parse_device_history(filename: str) -> List[DeviceHistory]:
    """
    Extracts the device history from a standard account.html file.

    :param filename: the path to the html file containing the device history data
    :return: a DeviceHistory object
    """
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    headers = soup.find_all(HtmlHeaders.H3.value)

    if len(headers) != len(HTML_HEADERS):
        raise ValueError(f"Unexpected number of {HtmlHeaders.H3.value} headers. Expected {len(HTML_HEADERS)}, found {len(headers)}")

    for i in range(len(HTML_HEADERS)):
        if headers[i].text != HTML_HEADERS[i]:
            raise ValueError(f"Unexpected {HtmlHeaders.H3.value} header at position {i}. Expected '{HTML_HEADERS[i]}', found '{headers[i].text}'")

    tables = soup.find_all(TableElements.TABLE.value)
    device_history_table = tables[2]
    rows = device_history_table.find_all(TableElements.TABLE_ROW.value)

    device_histories = [__parse_device_history_html(row) for row in rows]
    return device_histories

def parse_login_history(filename: str) -> List[LoginHistory]:
    """
    Extracts the login history from a standard account.html file.

    :param filename: the path to the html file containing the login history data
    :return: a LoginHistory object
    """
    pass
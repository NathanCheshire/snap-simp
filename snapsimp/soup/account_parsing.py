from datetime import datetime
import re
from typing import List
from common.basic_user_info import BasicUserInfo
from common.device_info import DeviceInformation
from common.device_history import DeviceHistory
from common.login_history import LoginHistory
from soup.device_information_row_indicie import DeviceInformationRowIndicie
from soup.basic_user_info_row_indicie import BasicUserInfoRowIndicie
from soup.login_history_label import LoginHistoryLabel
from soup.device_history_label import DeviceHistoryLabel
from soup.account_table import AccountTable
from soup.html_headers import HtmlHeaders
from soup.table_elements import TableElements
from bs4 import BeautifulSoup


def __get_soup_and_check_headers(filename: str) -> BeautifulSoup:
    """
    Reads the html file provided and confirms it looks like a standard account.html file.

    :param filename: the path to the account.html file
    :return: a beautiful soup object
    """
    with open(filename, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    headers = soup.find_all(HtmlHeaders.H3.value)

    if len(headers) != len(AccountTable):
        raise ValueError(f"Unexpected number of {HtmlHeaders.H3.value} headers. Expected {len(AccountTable)}, found {len(headers)}")

    for i, info_table in enumerate(AccountTable):
        if headers[i].text.lower() != info_table.name.replace('_', ' ').lower():
            raise ValueError(f"Unexpected {HtmlHeaders.H3.value} header at position {i}. Expected '{info_table.name.replace('_', ' ')}', found '{headers[i].text}'")
        
    return soup


def parse_basic_user_info(filename: str) -> BasicUserInfo:
    """
    Extracts the basic information from a standard account.html file.

    :param filename: the path to the html file containing the account data
    :return: a BasicUserInfo object
    """
    table = __get_soup_and_check_headers(filename).find(TableElements.TABLE.value)
    rows = table.find_all(TableElements.TABLE_ROW.value)

    username_row = rows[BasicUserInfoRowIndicie.USERNAME_ROW.value]
    name_row = rows[BasicUserInfoRowIndicie.NAME_ROW.value]
    creation_date_row = rows[BasicUserInfoRowIndicie.CREATION_DATE_ROW.value]

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
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    device_information_table = tables[1]

    rows = device_information_table.find_all(TableElements.TABLE_ROW.value)

    make_row = rows[DeviceInformationRowIndicie.MAKE_ROW.value]
    model_row = rows[DeviceInformationRowIndicie.MODEL_ROW.value]
    model_name_row = rows[DeviceInformationRowIndicie.MODEL_NAME_ROW.value]
    user_agent_row = rows[DeviceInformationRowIndicie.USER_AGENT_ROW.value]
    language_row = rows[DeviceInformationRowIndicie.LANGUAGE_ROW.value]
    os_type_row = rows[DeviceInformationRowIndicie.OS_TYPE_ROW.value]
    os_version_row = rows[DeviceInformationRowIndicie.OS_VERSION_ROW.value]
    connection_type_row = rows[DeviceInformationRowIndicie.CONNECTION_TYPE_ROW.value]

    make = make_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    model_id = model_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    model_name = model_name_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    user_agent = user_agent_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    language = language_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    os_type = os_type_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    os_version = os_version_row.find_all(TableElements.TABLE_HEADER.value)[1].text
    connection_type = [type.strip() for type in connection_type_row.find_all(TableElements.TABLE_HEADER.value)[1].text.split(',')]

    return DeviceInformation(make, model_id, model_name, user_agent, language, os_type, os_version, connection_type)


def __parse_device_history_row(row) -> DeviceHistory:
    """
    Extracts the device history from a BeautifulSoup row object.

    :param row: BeautifulSoup object representing a table row containing the device history data
    :return: a DeviceHistory object
    """
    row_str = re.sub("<.*?>", "", str(row))
    device_info = {}

    labels = list(DeviceHistoryLabel.__members__.values())

    for i in range(len(labels)-1):
        start = row_str.find(str(labels[i].value)) + len(str(labels[i].value))
        end = row_str.find(str(labels[i+1].value))
        device_info[labels[i].value] = row_str[start:end].strip()

    device_info[labels[-1].value] = row_str[row_str.find(str(labels[-1].value)) + len(str(labels[-1].value)):].strip()

    return DeviceHistory(
        make=device_info[DeviceHistoryLabel.MAKE.value],
        model=device_info[DeviceHistoryLabel.MODEL.value],
        start_time=device_info[DeviceHistoryLabel.START_TIME.value],
        device_type=device_info[DeviceHistoryLabel.DEVICE_TYPE.value]
    )


def parse_device_history(filename: str) -> List[DeviceHistory]:
    """
    Extracts the device history from a standard account.html file.

    :param filename: the path to the html file containing the device history data
    :return: a DeviceHistory object
    """
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    device_history_table = tables[2]
    rows = device_history_table.find_all(TableElements.TABLE_ROW.value)

    device_histories = [__parse_device_history_row(row) for row in rows]
    return device_histories


def __parse_login_history_row(row) -> LoginHistory:
    """
    Extracts the login history from a BeautifulSoup row object.

    :param row: BeautifulSoup object representing a table row containing the login history data
    :return: a LoginHistory object
    """
    row_str = re.sub("<.*?>", "", str(row))
    labels = [label.value for label in LoginHistoryLabel]
    login_info = {}

    for i in range(len(labels)-1):
        start = row_str.find(labels[i]) + len(labels[i])
        end = row_str.find(labels[i+1])
        login_info[labels[i]] = row_str[start:end].strip()

    login_info[labels[-1]] = row_str[row_str.find(labels[-1]) + len(labels[-1]):].strip()

    return LoginHistory(ip=login_info[LoginHistoryLabel.IP.value],
                        country=login_info[LoginHistoryLabel.COUNTRY.value],
                        created=login_info[LoginHistoryLabel.CREATED.value],
                        status=login_info[LoginHistoryLabel.STATUS.value],
                        device=login_info[LoginHistoryLabel.DEVICE.value])


TABLES_INDICIES = {

}

def parse_login_history(filename: str) -> List[LoginHistory]:
    """
    Extracts the login history from a standard account.html file.

    :param filename: the path to the html file containing the login history data
    :return: a LoginHistory object
    """
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    device_history_table = tables[3]
    rows = device_history_table.find_all(TableElements.TABLE_ROW.value)

    login_histories = [__parse_login_history_row(row) for row in rows]
    return login_histories

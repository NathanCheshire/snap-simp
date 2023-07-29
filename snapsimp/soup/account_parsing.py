import re
from typing import List, Tuple
from common.basic_user_info import BasicUserInfo
from common.device_info import DeviceInformation
from common.device_history import DeviceHistory
from common.login_history import LoginHistory
from soup.indicies.account_table_indicie import AccountTableIndicie
from soup.indicies.device_information_row_indicie import DeviceInformationRowIndicie
from soup.indicies.basic_user_info_row_indicie import BasicUserInfoRowIndicie
from common.login_history_label import LoginHistoryLabel
from common.device_history_label import DeviceHistoryLabel
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
    with open(filename, "r") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    headers = soup.find_all(HtmlHeaders.H3.value)

    if len(headers) != len(AccountTable):
        raise ValueError(
            f"Unexpected number of {HtmlHeaders.H3.value} headers. Expected {len(AccountTable)}, found {len(headers)}"
        )

    for i, info_table in enumerate(AccountTable):
        if headers[i].text.lower() != info_table.name.replace("_", " ").lower():
            raise ValueError(
                f"Unexpected {HtmlHeaders.H3.value} header at position {i}. Expected '{info_table.name.replace('_', ' ')}', found '{headers[i].text}'"
            )

    return soup


def parse_basic_user_info(filename: str) -> BasicUserInfo:
    """
    Extracts the basic information from a standard account.html file.

    :param filename: the path to the html file containing the account data
    :return: a BasicUserInfo object
    """
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    basic_user_info_table = tables[AccountTableIndicie.BASIC_USER_INFO.value]
    rows = basic_user_info_table.find_all(TableElements.TABLE_ROW.value)

    username_row = rows[BasicUserInfoRowIndicie.USERNAME_ROW.value]
    name_row = rows[BasicUserInfoRowIndicie.NAME_ROW.value]
    creation_date_row = rows[BasicUserInfoRowIndicie.CREATION_DATE_ROW.value]

    username = (
        username_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()
    )
    name = name_row.find_all(TableElements.TABLE_HEADER.value)[1].get_text().strip()
    creation_date = (
        creation_date_row.find_all(TableElements.TABLE_HEADER.value)[1]
        .get_text()
        .strip()
    )

    return BasicUserInfo(username, name, creation_date)


def parse_device_information(filename: str) -> DeviceInformation:
    """
    Extracts the device information from a standard account.html file.

    :param filename: the path to the html file containing the device information data
    :return: a DeviceInformation object
    """
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    device_information_table = tables[AccountTableIndicie.DEVICE_INFO.value]
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
    connection_type = [
        type.strip()
        for type in connection_type_row.find_all(TableElements.TABLE_HEADER.value)[
            1
        ].text.split(",")
    ]

    return DeviceInformation(
        make,
        model_id,
        model_name,
        user_agent,
        language,
        os_type,
        os_version,
        connection_type,
    )


def __parse_device_history_row(row) -> DeviceHistory:
    """
    Extracts the device history from a BeautifulSoup row object.

    :param row: BeautifulSoup object representing a table row containing the device history data
    :return: a DeviceHistory object
    """
    device_info = {}

    soup = BeautifulSoup(str(row), "html.parser")

    for label in DeviceHistoryLabel.values():
        tag = soup.find("b", text=re.compile(f"^{label.value}"))
        if tag:
            value = tag.next_sibling
            if value:
                if label == DeviceHistoryLabel.DEVICE_TYPE:
                    device_info[label.value] = value.strip().lower()
                else:
                    device_info[label.value] = value.strip()

    return DeviceHistory(
        make=device_info.get(DeviceHistoryLabel.MAKE.value, None),
        model=device_info.get(DeviceHistoryLabel.MODEL.value, None),
        start_time=device_info.get(DeviceHistoryLabel.START_TIME.value, None),
        device_type=device_info.get(DeviceHistoryLabel.DEVICE_TYPE.value, None),
    )


def parse_device_history(filename: str) -> List[DeviceHistory]:
    """
    Extracts the device history from a standard account.html file.

    :param filename: the path to the html file containing the device history data
    :return: a DeviceHistory object
    """
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    device_history_table = tables[AccountTableIndicie.DEVICE_HISTORY.value]
    rows = device_history_table.find_all(TableElements.TABLE_ROW.value)

    device_histories = [__parse_device_history_row(row) for row in rows]
    return device_histories


def __parse_login_history_row(row) -> LoginHistory:
    """
    Extracts the login history from a BeautifulSoup row object.

    :param row: BeautifulSoup object representing a table row containing the login history data
    :return: a LoginHistory object
    """
    login_info = {}

    soup = BeautifulSoup(str(row), "html.parser")

    for label in LoginHistoryLabel.values():
        tag = soup.find("b", text=re.compile(f"^{label.value}"))
        if tag:
            value = tag.next_sibling
            if value:
                login_info[label.value] = value.strip()

    return LoginHistory(
        ip=login_info.get(LoginHistoryLabel.IP.value, None),
        country=login_info.get(LoginHistoryLabel.COUNTRY.value, None),
        created=login_info.get(LoginHistoryLabel.CREATED.value, None),
        status=login_info.get(LoginHistoryLabel.STATUS.value, None),
        device=login_info.get(LoginHistoryLabel.DEVICE.value, None),
    )


def parse_login_history(filename: str) -> List[LoginHistory]:
    """
    Extracts the login history from a standard account.html file.

    :param filename: the path to the html file containing the login history data
    :return: a LoginHistory object
    """
    tables = __get_soup_and_check_headers(filename).find_all(TableElements.TABLE.value)
    device_history_table = tables[AccountTableIndicie.LOGIN_HISTORY.value]
    rows = device_history_table.find_all(TableElements.TABLE_ROW.value)

    login_histories = [__parse_login_history_row(row) for row in rows]
    return login_histories


def parse_all(
    filename: str,
) -> Tuple[BasicUserInfo, DeviceInformation, List[DeviceHistory], List[LoginHistory]]:
    """
    Parses and returns all data tables from the provided account.html file.

    :param filename: the path to the html file
    :return: a tuple containing the basic user info, device information, device history, and login history
    """
    basic_user_info = parse_basic_user_info(filename)
    device_information = parse_device_information(filename)
    device_history = parse_device_history(filename)
    login_history = parse_login_history(filename)

    return basic_user_info, device_information, device_history, login_history

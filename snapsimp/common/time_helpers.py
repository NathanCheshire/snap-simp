from datetime import timedelta
import datetime
from typing import List


def _daterange(start_date: datetime.date, end_date: datetime.date) -> datetime.date:
    """
    Generates a range of dates from start_date to end_date (inclusive).
    
    :param start_date: The start date of the range
    :param end_date: The end date of the range

    :yield: each date in the range
    """

    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)


def generate_ordered_date_range(min_date: datetime.date, max_date: datetime.date, ascending = True) -> List[datetime.date]:
    """
    Generate an ordered list of dates between a given start and end date.
    
    :param min_date: the earliest date (inclusive) in the range
    :param max_date: the latest date (inclusive) in the range
    :param ascending: if True, the dates will be sorted in ascending order.
                      If False, the dates will be sorted in descending order.
                      Default is True

    :return: a list of dates between the start and end date, ordered according to the 'ascending' parameter
    """

    all_days = set(_daterange(min_date, max_date))
    all_days_list = list(all_days)
    all_days_sorted = sorted(all_days_list, reverse=(not ascending))
    return all_days_sorted
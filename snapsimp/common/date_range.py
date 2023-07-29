from datetime import datetime, timedelta


class DateRange:
    def __init__(self, start_date: datetime, end_date: datetime):
        assert (
            start_date <= end_date
        ), "Start date must be less than or equal to end date"
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self):
        return f"DateRange(start_date={self.start_date}, end_date={self.end_date})"

    def duration(self) -> timedelta:
        """Get the duration of the date range."""
        return self.end_date - self.start_date

    def contains(self, date: datetime) -> bool:
        """Check if a date is within the date range."""
        return self.start_date <= date <= self.end_date

    def overlaps(self, other: "DateRange") -> bool:
        """Check if this date range overlaps with another date range."""
        return max(self.start_date, other.start_date) <= min(
            self.end_date, other.end_date
        )

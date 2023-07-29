from datetime import timedelta


class DescriptiveStats:
    def __init__(self, minimum, average, maximum):
        self.minimum = minimum
        self.average = average
        self.maximum = maximum

    def __repr__(self):
        return f"{self.__class__.__name__}(minimum={self.minimum}, average={self.average}, maximum={self.maximum})"

    def __str__(self):
        return f"Min: {self.minimum}, Avg: {self.average}, Max: {self.maximum}"


class DescriptiveStatsFloat(DescriptiveStats):
    def __init__(self, minimum: float, average: float, maximum: float):
        super().__init__(minimum, average, maximum)


class DescriptiveStatsTimedelta(DescriptiveStats):
    def __init__(self, minimum: timedelta, average: timedelta, maximum: timedelta):
        super().__init__(minimum, average, maximum)

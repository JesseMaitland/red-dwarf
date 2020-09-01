from enum import Enum
from typing import List


class BaseEnum(Enum):

    @classmethod
    def members(cls) -> List[str]:
        return [x.name for x in cls]


class ExecutionMethods(BaseEnum):
    ONCE = 1
    INCREMENTAL = 2
    ONCE_INCREMENTAL = 3


class ExecutionIntervals(BaseEnum):
    HOURS = 1
    DAYS = 2
    MONTHS = 3
    YEARS = 4
    DATES = 5

from datetime import date, timedelta
from typing import Tuple, Any

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import big_int
from py_message_encoder.message_types import MessageType


REFERENCE_DATE: date = date.fromtimestamp(0)


class DateEncoder(PartialEncoder):
    def __init__(self):
        super(DateEncoder, self).__init__(MessageType.DATE)

    def encode(self, value: date) -> str:
        value.ctime()
        total_days = (value - REFERENCE_DATE).days
        return big_int.encode(total_days)

    def decode_value(self, value: str) -> Tuple[date, int]:
        total_days, consumed = big_int.decode_value(value)
        _date = REFERENCE_DATE + timedelta(days=total_days)
        return _date, consumed


class TimeEncoder(PartialEncoder):
    def encode(self, value) -> str:
        pass

    def decode_value(self, value: str) -> Tuple[Any, int]:
        pass


class DateTimeEncoder(PartialEncoder):
    def encode(self, value) -> str:
        pass

    def decode_value(self, value: str) -> Tuple[Any, int]:
        pass


date_encoder = DateEncoder()

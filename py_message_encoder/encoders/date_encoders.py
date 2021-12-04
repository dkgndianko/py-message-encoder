from datetime import date, timedelta, time, datetime, timezone
from typing import Tuple

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import big_int
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import custom_base_64

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
    def __init__(self):
        super(TimeEncoder, self).__init__(MessageType.TIME)

    def encode(self, value: time) -> str:
        seconds = value.hour * 3600 + value.minute * 60 + value.second
        # supports offset ranging from -12 to +15 (+14 + DST)
        # offset should multiplier of 0.5 hours (xx hours or xx.5 hours only are supported)
        offset = value.utcoffset()
        if offset:
            offset //= timedelta(minutes=30)
        else:
            offset = 0
        offset += 24  # normalize to avoid negative numbers by adding 12 hours (24 x 0.5 hours)
        return custom_base_64.encode(offset) + big_int.encode(seconds)

    def decode_value(self, value: str) -> Tuple[time, int]:
        offset = custom_base_64.decode(value[0])
        offset -= 24
        offset_timedelta = timedelta(minutes=offset * 30)
        seconds, consumed = big_int.decode_value(value[1:])
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        _time = time(hour=hours, minute=minutes, second=seconds, tzinfo=timezone(offset_timedelta))
        return _time, consumed + 1


class DateTimeEncoder(PartialEncoder):
    def __init__(self):
        super(DateTimeEncoder, self).__init__(MessageType.DATE_TIME)

    def encode(self, value: datetime) -> str:
        pass

    def decode_value(self, value: str) -> Tuple[datetime, int]:
        pass


date_encoder = DateEncoder()
time_encoder = TimeEncoder()

from typing import Tuple

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import big_int
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import left_pad


class FloatEncoder(PartialEncoder):

    def __init__(self, precision: int = 6):
        super(FloatEncoder, self).__init__(MessageType.FLOAT)
        self.precision = precision

    def encode(self, value: float) -> str:
        value = round(value, self.precision)
        _decimal_part = ""
        if value.is_integer():
            _int_part = str(int(value))
        else:
            _int_part, _decimal_part = str(value).split(".")  # issue with scientific notation i.e 8.9e-10
        _decimal_part = _decimal_part.rstrip("0")
        _int_part = _int_part.lstrip("0")
        representation = f"{_int_part}{_decimal_part}{left_pad(str(len(_int_part)), 2, '0')}"
        return big_int.encode(int(representation))

    def decode_value(self, value: str) -> Tuple[float, int]:
        whole, consumed = big_int.decode_value(value)
        whole, _int_part_len = divmod(whole, 100)
        whole = str(whole)
        _int_part = whole[:_int_part_len]
        _decimal_part = whole[_int_part_len:]
        return float(f"{_int_part or '0'}.{_decimal_part or '0'}"), consumed

    def __str__(self):
        return "Float Encoder"


float_encoder = FloatEncoder()




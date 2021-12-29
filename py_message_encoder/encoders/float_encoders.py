from typing import Tuple, Any

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import big_int, unsigned_tiny_int
from py_message_encoder.message_types import MessageType


class FloatEncoder(PartialEncoder):

    def __init__(self, precision: int = 6):
        super(FloatEncoder, self).__init__(MessageType.FLOAT)
        self.precision = precision

    def min_length(self):
        return unsigned_tiny_int.min_length() + big_int.min_length()

    def max_length(self):
        return unsigned_tiny_int.max_length() + big_int.max_length()

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        return isinstance(value, float), "Can only encode floats"

    def encode_value(self, value: float) -> str:
        value = round(value, self.precision)
        _decimal_part = ""
        if value.is_integer():
            _int_part = str(int(value))
        else:
            _int_part, _decimal_part = str(value).split(".")  # issue with scientific notation i.e 8.9e-10
        _decimal_part = _decimal_part.rstrip("0")
        _int_part = _int_part.lstrip("0")
        _int_part_len = len(_int_part) + 15
        representation = f"{_int_part}{_decimal_part}" or "0"
        _whole_len = len(representation)
        zero_index = 0
        while zero_index < _whole_len and representation[zero_index] == "0":
            zero_index += 1
        _int_part_len -= zero_index
        return unsigned_tiny_int.encode(_int_part_len) + big_int.encode(int(representation))

    def decode_value(self, value: str) -> Tuple[float, int]:
        _int_part_len, _int_part_len_digits = unsigned_tiny_int.decode_value(value)
        _int_part_len -= 15
        _decimal_padding = ""
        if _int_part_len < 0:
            _decimal_padding = "0" * (-_int_part_len)
            _int_part_len = 0
        whole, consumed = big_int.decode_value(value[_int_part_len_digits:])
        whole = str(whole)
        _int_part = whole[:_int_part_len]
        _decimal_part = _decimal_padding + whole[_int_part_len:]
        return float(f"{_int_part or '0'}.{_decimal_part or '0'}"), consumed + _int_part_len_digits

    def __str__(self):
        return "Float Encoder"


float_encoder = FloatEncoder()




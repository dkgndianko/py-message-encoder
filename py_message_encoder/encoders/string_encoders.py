from typing import Tuple

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import left_pad, right_pad, custom_base_64


class FixedLengthEncoder(PartialEncoder):
    def __init__(self, length: int):
        super(FixedLengthEncoder, self).__init__(MessageType.FIXED_LENGTH_STRING)
        self._length: int = length

    def length(self) -> int:
        return self._length

    def encode(self, value: str) -> str:
        _len = len(value)
        if _len >= self.length():
            return value[:self._length]
        else:
            diff = self._length - _len
            return right_pad(value, self._length, ' ')

    def decode_value(self, value: str) -> Tuple[str, int]:
        return value.rstrip(), self._length

    def __str__(self):
        return f"Fixed Length String Encoder ({self._length})"


class VariableLengthEncoder(PartialEncoder):
    def __init__(self, length_digits):
        super(VariableLengthEncoder, self).__init__(MessageType.VARIABLE_LENGTH_STRING)
        self.length_digits = length_digits
        self._max_length = custom_base_64.alphabet_len ** self.length_digits - 1
        self._max_global_length = self.length_digits + self._max_length

    def max_length(self):
        return self._max_length

    def min_length(self):
        return self.length_digits

    def max_global_length(self):
        return self._max_global_length

    def encode(self, value: str) -> str:
        _len = len(value)
        if _len > self.max_length():
            raise ValueError(f"This can only encode strings with length at most {self.max_length()}. {_len} given.")
        # _len = hex(_len)[2:]
        _len = custom_base_64.encode(_len)
        _len = left_pad(str(_len), self.length_digits, custom_base_64.zero)
        return f"{_len}{value}"

    def decode_value(self, value: str) -> Tuple[str, int]:
        global_length = len(value)
        # if global_length < self.length_digits or global_length > (self.max_length() + self.length_digits):
        #     raise ValueError(f"The value should have length between {self.length_digits} and {self._max_global_length}")
        _len = value[:self.length_digits]
        _len = custom_base_64.decode(_len)
        _value = value[self.length_digits:_len + 1]
        if len(_value) != _len:
            raise ValueError(f"{len(_value)} != {_len}")
        return _value, _len + self.length_digits

    def __str__(self):
        return f"Variable Length String Encoder (length digits: {self.length_digits}, max length: {self._max_length}) "


LVAR = VariableLengthEncoder(1)
LLVAR = VariableLengthEncoder(2)
LLLVAR = VariableLengthEncoder(3)

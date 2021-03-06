from typing import Tuple, Any

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import left_pad, custom_unsigned_base_64


class StringEncoderMixin:

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        if isinstance(value, str) and len(value) <= self.max_length():
            return True, ""
        else:
            return False, f"This can only encode strings with length at most {self.max_length()}."


class FixedLengthEncoder(StringEncoderMixin, PartialEncoder):
    def __init__(self, length: int, padding_char: str = ' '):
        assert not padding_char or len(padding_char) == 1, "Give only one character for padding"
        super(FixedLengthEncoder, self).__init__(MessageType.FIXED_LENGTH_STRING)
        self._length: int = length
        self._padding_char = padding_char or ' '

    def length(self) -> int:
        return self._length

    def encode_value(self, value: str) -> str:
        _len = len(value)
        if _len >= self.length():
            return value[:self._length]
        else:
            return left_pad(value, self._length, self._padding_char)

    def decode_value(self, value: str) -> Tuple[str, int]:
        return value[: self._length].lstrip(self._padding_char), self._length

    def __str__(self):
        return f"Fixed Length String Encoder ({self._length})"


class VariableLengthEncoder(StringEncoderMixin, PartialEncoder):
    def __init__(self, length_digits: int):
        assert length_digits > 0, "Length should be greater than 0"
        PartialEncoder.__init__(self, MessageType.VARIABLE_LENGTH_STRING)
        self.length_digits = length_digits
        self._max_length = custom_unsigned_base_64.max_encodable_with_len(self.length_digits)
        self._max_global_length = self.length_digits + self._max_length

    def max_length(self):
        return self._max_length

    def min_length(self):
        return self.length_digits

    def max_global_length(self):
        return self._max_global_length

    def encode_value(self, value: str) -> str:
        _len = custom_unsigned_base_64.encode(len(value))
        _len = left_pad(str(_len), self.length_digits, custom_unsigned_base_64.zero)
        return f"{_len}{value}"

    def decode_value(self, value: str) -> Tuple[str, int]:
        _len_digits = self.length_digits
        assert len(value) >= _len_digits, f"Should at least have {_len_digits} characters. But only {len(value)}."
        _len = value[:_len_digits]
        _len = custom_unsigned_base_64.decode(_len)
        _value = value[_len_digits: _len_digits + _len]
        if len(_value) != _len:
            raise ValueError(f"Length should be {_len}, but only {len(_value)} was read.")
        return _value, _len + _len_digits

    def __str__(self):
        return f"Variable Length String Encoder (length digits: {self.length_digits}, max length: {self._max_length}) "


LVAR = VariableLengthEncoder(1)
LLVAR = VariableLengthEncoder(2)
LLLVAR = VariableLengthEncoder(3)

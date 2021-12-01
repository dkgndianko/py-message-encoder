from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import left_pad, right_pad


class FixedLengthEncoder(PartialEncoder):
    def __init__(self, length):
        super(FixedLengthEncoder, self).__init__(MessageType.FIXED_LENGTH_STRING)
        self._length = length

    def length(self) -> int:
        return self._length

    def encode(self, value: str) -> str:
        _len = len(value)
        if _len >= self.length():
            return value[:self._length]
        else:
            diff = self._length - _len
            return right_pad(value, self._length, ' ')

    def decode(self, value: str) -> str:
        return value.rstrip()


class VariableLengthEncoder(PartialEncoder):
    def __init__(self, length_digits):
        super(VariableLengthEncoder, self).__init__(MessageType.VARIABLE_LENGTH_STRING)
        self.length_digits = length_digits
        self._max_length = 10 ** self.length_digits - 1
        self._max_global_length = self.length_digits + self._max_length

    def max_length(self):
        return self._max_length

    def max_global_length(self):
        return self._max_global_length

    def encode(self, value: str) -> str:
        _len = len(value)
        if _len > self.max_length():
            raise ValueError(f"This can only encode strings with length at most {self.max_length()}. {_len} given.")
        _len = left_pad(str(_len), self.length_digits, '0')
        return f"{_len}{value}"

    def decode(self, value: str) -> str:
        global_length = len(value)
        if global_length < self.length_digits or global_length > (self.max_length() + self.length_digits):
            raise ValueError(f"The value should have length between {self.length_digits} and {self._max_global_length}")
        _len = value[:self.length_digits]
        try:
            _len = int(_len)
        except:
            raise ValueError()
        _value = value[self.length_digits:]
        if len(_value) != _len:
            raise ValueError()
        return _value


LVAR = VariableLengthEncoder(1)
LLVAR = VariableLengthEncoder(2)
LLLVAR = VariableLengthEncoder(3)

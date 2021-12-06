from typing import Tuple

from py_message_encoder.encoders.string_encoders import VariableLengthEncoder, FixedLengthEncoder
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import custom_base_64


class CappedValue:
    def __init__(self, max_value):
        self.max_value = max_value

    def check_bound(self, value):
        if value > self.max_value:
            raise ValueError(f"The value is greater that {self.max_value}")


class _IntFixedLengthEncoder(FixedLengthEncoder, CappedValue):
    def __init__(self, max_value: int):
        super(_IntFixedLengthEncoder, self).__init__(len(str(max_value)), '0')
        self.message_type = MessageType.INT
        CappedValue.__init__(self, max_value)

    def encode(self, value: int) -> str:
        self.check_bound(value)
        return super(_IntFixedLengthEncoder, self).encode(str(value))

    def decode_value(self, value: str) -> Tuple[int, int]:
        _val = super(_IntFixedLengthEncoder, self).decode_value(value)
        return int(_val), self.length()

    def __str__(self):
        return f"Integer with fixed length encoder (max: {self.max_value}, length: {self.length()})"


class IntFixedLengthEncoder(FixedLengthEncoder, CappedValue):
    def __init__(self, max_value: int):
        super(IntFixedLengthEncoder, self).__init__(len(str(max_value)), custom_base_64.zero)
        self.message_type = MessageType.INT
        CappedValue.__init__(self, max_value)

    def encode(self, value: int) -> str:
        self.check_bound(value)
        return super(IntFixedLengthEncoder, self).encode(custom_base_64.encode(value))

    def decode_value(self, value: str) -> Tuple[int, int]:
        _val = super(IntFixedLengthEncoder, self).decode_value(value)
        return custom_base_64.decode(_val), self.length()

    def __str__(self):
        return f"Integer base64 encoded with fixed length encoder (max: {self.max_value}, length: {self.length()})"


class IntegerVarLengthEncoder(VariableLengthEncoder):
    def __init__(self,):
        super(IntegerVarLengthEncoder, self).__init__(1)
        self.message_type = MessageType.INT

    def encode(self, value: int) -> str:
        return super(IntegerVarLengthEncoder, self).encode(custom_base_64.encode(value))

    def decode_value(self, value: str) -> Tuple[int, int]:
        _val, _consumed = super(IntegerVarLengthEncoder, self).decode_value(value)
        return custom_base_64.decode(_val), _consumed

    def __str__(self):
        return f"Integer with variable length encoder (length digits: {self.length_digits}, max length: {self._max_length})"


small_int = IntFixedLengthEncoder(255)
_small_int = _IntFixedLengthEncoder(255)
big_int = IntegerVarLengthEncoder()

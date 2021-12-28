from typing import Tuple, Any

from py_message_encoder.encoders.string_encoders import VariableLengthEncoder, FixedLengthEncoder
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import custom_base_64, custom_unsigned_base_64, CustomIntegerBaseMixin


class CappedIntMixin:
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value
        self.message_type = MessageType.INT

    def check_bound(self, value):
        if value > self.max_value or value < self.min_value:
            raise ValueError(f"The value should be in range [{self.min_value} ... {self.max_value}]")

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        try:
            assert isinstance(value, int), "Cannot encode non int values"
            self.check_bound(value)
        except (ValueError, AssertionError) as e:
            return False, str(e)
        else:
            return True, ""


class _IntFixedLengthEncoder(FixedLengthEncoder, CappedIntMixin):
    def __init__(self, length: int):
        super(_IntFixedLengthEncoder, self).__init__(length, '0')
        CappedIntMixin.__init__(self, -(10**(length - 1) - 1), 10**length - 1)

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        return CappedIntMixin.can_encode(self, value)

    def encode_value(self, value: int) -> str:
        return super(_IntFixedLengthEncoder, self).encode_value(str(value))

    def decode_value(self, value: str) -> Tuple[int, int]:
        _val, consumed = super(_IntFixedLengthEncoder, self).decode_value(value)
        return int(_val), consumed

    def __str__(self):
        return f"Integer with fixed length encoder (max: {self.max_value}, length: {self.length()})"


class IntFixedLengthEncoderMixin(FixedLengthEncoder, CappedIntMixin):
    def __init__(self, length: int, encoder: CustomIntegerBaseMixin = custom_base_64):
        super(IntFixedLengthEncoderMixin, self).__init__(length, encoder.zero)
        _max = encoder.max_encodable_with_len(length)
        CappedIntMixin.__init__(self, -_max, _max)
        self.encoder = encoder

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        return CappedIntMixin.can_encode(self, value)

    def encode_value(self, value: int) -> str:
        return super(IntFixedLengthEncoderMixin, self).encode_value(self.encoder.encode(value))

    def decode_value(self, value: str) -> Tuple[int, int]:
        _val, consumed = super(IntFixedLengthEncoderMixin, self).decode_value(value)
        return self.encoder.decode(_val), consumed

    def __str__(self):
        return f"Integer base64 encoded with fixed length encoder (max: {self.max_value}, length: {self.length()})"


class IntFixedLengthEncoder(IntFixedLengthEncoderMixin):
    def __init__(self, length: int):
        super(IntFixedLengthEncoder, self).__init__(length, custom_base_64)


class UnsignedIntFixedLengthEncoder(IntFixedLengthEncoderMixin):
    def __init__(self, length: int):
        super(UnsignedIntFixedLengthEncoder, self).__init__(length, custom_unsigned_base_64)

    def __str__(self):
        return f"Unsigned Integer base64 encoded with fixed length encoder (max: {self.max_value}, length: " \
               f"{self.length()}) "


class IntegerVarLengthEncoder(VariableLengthEncoder, CappedIntMixin):
    def __init__(self, len_digits: int = 1):
        super(IntegerVarLengthEncoder, self).__init__(len_digits)
        max_encodable = custom_base_64.max_encodable_with_len(self._max_length)
        CappedIntMixin.__init__(self, -max_encodable, max_encodable)

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        return CappedIntMixin.can_encode(self, value)

    def encode_value(self, value: int) -> str:
        return super(IntegerVarLengthEncoder, self).encode_value(custom_base_64.encode(value))

    def decode_value(self, value: str) -> Tuple[int, int]:
        _val, _consumed = super(IntegerVarLengthEncoder, self).decode_value(value)
        return custom_base_64.decode(_val), _consumed

    def __str__(self):
        return f"Integer with variable length encoder (length digits: {self.length_digits}, max length: {self._max_length})"


small_int = IntFixedLengthEncoder(2)
unsigned_tiny_int = UnsignedIntFixedLengthEncoder(1)
_small_int = _IntFixedLengthEncoder(2)
big_int = IntegerVarLengthEncoder()

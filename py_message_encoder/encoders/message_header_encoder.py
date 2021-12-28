from typing import Tuple, Any

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import big_int, unsigned_small_int
from py_message_encoder.header import MessageHeader
from py_message_encoder.message_types import MessageType
from py_message_encoder.utilities import custom_binary, left_pad


class MessageHeaderEncoder(PartialEncoder):

    def __init__(self):
        super(MessageHeaderEncoder, self).__init__(MessageType.HEADER)
        self._min_length = big_int.min_length() + unsigned_small_int.length()

    def min_length(self) -> int:
        return self._min_length

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        _can, _msg = super(MessageHeaderEncoder, self).can_encode(value)
        if _can is False:
            return False, _msg
        if value.number_of_parts > unsigned_small_int.max_value:
            return False, f"Number of parts cannot be up to {unsigned_small_int.max_value}"
        return True, ""

    def encode_value(self, value: MessageHeader) -> str:
        _len = value.number_of_parts
        _value_dumped = value.dump()
        _dump_int = custom_binary.decode(_value_dumped)
        return unsigned_small_int.encode(_len) + big_int.encode(_dump_int)

    def decode_value(self, value: str) -> Tuple[MessageHeader, int]:
        _len, consumed_1 = unsigned_small_int.decode_value(value)
        _dump_int, consumed_2 = big_int.decode_value(value[consumed_1:])
        _dumped = custom_binary.encode(_dump_int)
        _dumped = left_pad(_dumped, _len, "0")
        mh = MessageHeader.parse(_dumped)
        return mh, consumed_1 + consumed_2

    def __str__(self):
        return f"Message Header encoder"


header_encoder = MessageHeaderEncoder()

from typing import Tuple, Any, List

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import big_int
from py_message_encoder.message_types import MessageType


class HomogenousListEncoder(PartialEncoder):

    def __init__(self, base_encoder: PartialEncoder):
        self.base_encoder = base_encoder
        super(HomogenousListEncoder, self).__init__(MessageType.LIST)

    def min_length(self):
        return big_int.min_length()  # empty list

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        # TODO 1: think about other iterables
        #      2: verify if each element is encodable (self.base_encoder.can_encode(e) for e in value)
        return isinstance(value, list), "Can only encode lists"

    def encode_value(self, value: List) -> str:
        _len = big_int.encode(len(value))
        return _len + "".join(self.base_encoder.encode(v) for v in value)

    def decode_value(self, value: str) -> Tuple[List[Any], int]:
        result = []
        _len, consumed = big_int.decode_value(value)
        for i in range(_len):
            try:
                v, _consumed = self.base_encoder.decode_value(value[consumed:])
            except (ValueError, AssertionError) as e:
                raise ValueError(f"Error when decoding item {i+1}/{_len} of list. {e}") from e
            consumed += _consumed
            result.append(v)
        return result, consumed

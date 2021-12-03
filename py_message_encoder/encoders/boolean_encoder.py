from typing import Tuple

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.message_types import MessageType


class BooleanEncoder(PartialEncoder):
    def __init__(self):
        super(BooleanEncoder, self).__init__(MessageType.BOOLEAN)

    def length(self) -> int:
        return 1

    def encode(self, value) -> str:
        return "1" if value else "0"

    def decode_value(self, value: str) -> Tuple[bool, int]:
        # verify if the value is "0" or "1"
        return value == "1", 1

    def __str__(self):
        return "Boolean Encoder"

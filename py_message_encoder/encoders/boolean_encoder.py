from typing import Any

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.message_types import MessageType


class BooleanEncoder(PartialEncoder):
    def __init__(self):
        super(BooleanEncoder, self).__init__(MessageType.BOOLEAN)

    def length(self) -> int:
        return 1

    def encode(self, value) -> str:
        return "1" if value else "0"

    def decode(self, value: str) -> Any:
        # verify if the value is "0" or "1"
        return value == "1"

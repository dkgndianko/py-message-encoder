from typing import Any

from py_message_encoder.message_types import MessageType


class PartialEncoder:
    def __init__(self, message_type: MessageType):
        self.message_type = message_type

    def length(self) -> int:
        return 0

    def max_length(self):
        return self.length()

    def encode(self, value) -> str:
        pass

    def decode(self, value: str) -> Any:
        pass

    def __str__(self):
        return ""

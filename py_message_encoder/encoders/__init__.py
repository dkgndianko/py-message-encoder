from abc import ABC, abstractmethod
from typing import Any, Tuple

from py_message_encoder.message_types import MessageType


class PartialEncoder(ABC):
    def __init__(self, message_type: MessageType):
        self.message_type = message_type

    def length(self) -> int:
        return 0

    def min_length(self):
        return self.length()

    def max_length(self):
        return self.length()

    def can_decode(self, value: str) -> bool:
        return isinstance(value, str) and len(value) >= self.min_length()

    def decode(self, value: str) -> Tuple[Any, str]:
        _min_len = self.min_length()
        _val_len = len(value)
        assert _val_len >= _min_len, f"Value should at least have {_min_len} characters."
        assert self.can_decode(value), f"cannot decode value '{value}'"
        decoded, _len_consumed = self.decode_value(value)
        assert (_min_len <= _len_consumed <= _val_len), f"cannot consumes less than {_min_len} or more than {_val_len} characters."
        return decoded, value[_len_consumed:]

    @abstractmethod
    def encode(self, value) -> str:
        pass

    @abstractmethod
    def decode_value(self, value: str) -> Tuple[Any, int]:
        pass

    def __str__(self):
        return ""

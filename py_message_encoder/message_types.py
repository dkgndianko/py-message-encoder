from datetime import datetime, date, time
from enum import Enum

from py_message_encoder.body import MessageBody
from py_message_encoder.header import MessageHeader


class MessageType(Enum):
    BOOLEAN = ("BOOLEAN", object)
    INT = ("INT", int)
    FIXED_LENGTH_STRING = ("FIXED_LENGTH_STRING", str)
    VARIABLE_LENGTH_STRING = ("VARIABLE_LENGTH_STRING", str)
    FLOAT = ("FLOAT", float)
    DATE = ("DATE", date)
    DATE_TIME = ("DATE_TIME", datetime)
    TIME = ("TIME", time)
    HEADER = ("HEADER", MessageHeader)
    BODY = ("BODY", MessageBody)
    LIST = ("LIST", list)

    def __str__(self):
        return self.name

    @property
    def target_type(self):
        return self.value[1]

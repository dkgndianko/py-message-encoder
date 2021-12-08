from collections import OrderedDict
from typing import Tuple, List

from py_message_encoder.body import MessageBody
from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.message_header_encoder import header_encoder
from py_message_encoder.header import MessageHeader
from py_message_encoder.message_types import MessageType


class MessageField:
    def __init__(self, name: str, encoder: PartialEncoder):
        self.name = name
        self.encoder = encoder


class FieldMapping:
    def __init__(self, fields: List[MessageField]):
        self.field_mapping = OrderedDict()
        for field in fields:
            if field.name in self.field_mapping:
                raise KeyError(f"Field name '{field.name}' is repeated.")
            self.field_mapping.update({field.name: field.encoder})
        self.names = self.field_mapping.keys()

    def items(self):
        return  self.field_mapping.items()

    def fields_count(self):
        return len(self.names)


class BodyEncoder(PartialEncoder):
    def __init__(self, field_mapping: FieldMapping):
        super(BodyEncoder, self).__init__(MessageType.BODY)
        self.field_mapping = field_mapping
        self.fields_count = self.field_mapping.fields_count()

    def encode_value(self, value: MessageBody) -> str:
        header = MessageHeader(value.fields_count())
        index = 0
        body = ""
        for name, encoder in self.field_mapping.items():
            try:
                data = value[name]
                header.set_presence(index, True)
                body += encoder.encode(data)
            except KeyError:
                pass
            index += 1
        return header_encoder.encode(header) + body

    def decode_value(self, value: str) -> Tuple[MessageBody, int]:
        header, consumed_header = header_encoder.decode_value(value)
        if header.number_of_parts != self.fields_count:
            raise ValueError(f"Header is not matching the correct number of parts. Expecting {self.fields_count} "
                             f"and got {header.number_of_parts}")
        body = MessageBody(list(self.field_mapping.names))
        index = 0
        consumed = consumed_header
        for name, encoder in self.field_mapping.items():
            if header.is_present(index):
                part, consumed_by_part = encoder.decode_value(value[consumed:])
                consumed += consumed_by_part
                body[name] = part
            index += 1
        return body, consumed

    def __str__(self):
        return f"Message Body Encoder (fields: {list(self.field_mapping.names)})"

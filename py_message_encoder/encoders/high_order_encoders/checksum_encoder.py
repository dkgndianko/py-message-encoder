from typing import Tuple, Any

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.encoders.integer_encoders import small_int
from py_message_encoder.utils.luhn import calculate_luhn


class ChecksumEncoder(PartialEncoder):
    def __init__(self, base_encoder: PartialEncoder):
        PartialEncoder.__init__(self, base_encoder.message_type)
        self.encoder = base_encoder

    def min_length(self):
        return self.encoder.min_length() + small_int.length()

    def can_encode(self, value: Any) -> Tuple[bool, str]:
        return self.encoder.can_encode(value)

    def encode_value(self, value) -> str:
        encoded = self.encoder.encode(value)
        checksum = calculate_checksum(encoded)
        return encoded + small_int.encode(checksum)

    def decode_value(self, value: str) -> Tuple[Any, int]:
        decoded, value_consumed = self.encoder.decode_value(value)
        read_checksum, checksum_consumed = small_int.decode_value(value[value_consumed:])
        if verify_checksum(value[:value_consumed], read_checksum) is False:
            raise ValueError("Checksum not matching")
        return decoded, value_consumed + checksum_consumed


def calculate_checksum(_input: str) -> int:
    return calculate_luhn(_input)


def verify_checksum(_input: str, proposed_checksum: int) -> bool:
    calculated = calculate_checksum(_input)
    return calculated == proposed_checksum


def with_checksum(encoder_class):
    class WithChecksumEncoder(encoder_class):
        def min_length(self):
            return super(WithChecksumEncoder, self).min_length() + small_int.length()

        def can_encode(self, value: Any) -> Tuple[bool, str]:
            return super(WithChecksumEncoder, self).can_encode(value)
    
        def encode_value(self, value) -> str:
            encoded = super(WithChecksumEncoder, self).encode(value)
            checksum = calculate_checksum(encoded)
            return encoded + small_int.encode(checksum)
    
        def decode_value(self, value: str) -> Tuple[Any, int]:
            decoded, value_consumed = super(WithChecksumEncoder, self).decode_value(value)
            read_checksum, checksum_consumed = small_int.decode_value(value[value_consumed:])
            if verify_checksum(value[:value_consumed], read_checksum) is False:
                raise ValueError("Checksum not matching")
            return decoded, value_consumed + checksum_consumed
    return WithChecksumEncoder

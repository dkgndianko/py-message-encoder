from py_message_encoder.encoders.string_encoders import VariableLengthEncoder, FixedLengthEncoder
from py_message_encoder.utilities import custom_base_64


class CappedValue:
    def __init__(self, max_value):
        self.max_value = max_value

    def check_bound(self, value):
        if value > self.max_value:
            raise ValueError(f"The value is greater that {self.max_value}")


class _IntFixedLengthEncoder(FixedLengthEncoder, CappedValue):
    def __init__(self, max_value: int):
        super(_IntFixedLengthEncoder, self).__init__(len(str(max_value)))
        CappedValue.__init__(self, max_value)

    def encode(self, value: int) -> str:
        self.check_bound(value)
        return super(_IntFixedLengthEncoder, self).encode(str(value))

    def decode(self, value: str) -> int:
        _val = super(_IntFixedLengthEncoder, self).decode(value)
        return int(_val)


class IntFixedLengthEncoder(FixedLengthEncoder, CappedValue):
    def __init__(self, max_value: int):
        super(IntFixedLengthEncoder, self).__init__(len(str(max_value)))
        CappedValue.__init__(self, max_value)

    def encode(self, value: int) -> str:
        self.check_bound(value)
        return super(IntFixedLengthEncoder, self).encode(custom_base_64.encode(value))

    def decode(self, value: str) -> int:
        _val = super(IntFixedLengthEncoder, self).decode(value)
        return custom_base_64.decode(_val)


class IntegerVarLengthEncoder(VariableLengthEncoder):
    def __init__(self,):
        super(IntegerVarLengthEncoder, self).__init__(1)

    def encode(self, value: int) -> str:
        return super(IntegerVarLengthEncoder, self).encode(custom_base_64.encode(value))

    def decode(self, value: str) -> int:
        _val = super(IntegerVarLengthEncoder, self).decode(value)
        return custom_base_64.decode(_val)


small_int = IntFixedLengthEncoder(255)
_small_int = _IntFixedLengthEncoder(255)
big_int = IntegerVarLengthEncoder()

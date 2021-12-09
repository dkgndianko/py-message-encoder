from py_message_encoder.encoders.string_encoders import VariableLengthEncoder
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class VariableLengthEncoderTest(EncoderTest):
    ENCODER_CLASS = VariableLengthEncoder
    FLAVORS = [(1,), (2, ), (3, )]

    @with_flavor(0)
    def test_can_encode(self):
        self.assertCanEncode("This is a medium text")
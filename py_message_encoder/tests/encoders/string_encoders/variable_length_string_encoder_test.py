from py_message_encoder.encoders.string_encoders import VariableLengthEncoder
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class VariableLengthEncoderTest(EncoderTest):
    ENCODER_CLASS = VariableLengthEncoder
    FLAVORS = [(1,), (2, ), (3, )]

    @with_flavor(0)
    def test_can_encode(self):
        self.assertCanEncode("This is a small text")
        self.assertCanEncode("This is a small text" * 3)
        self.assertCannotEncode("This is a medium text" * 23)
        self.assertCanEncode("This is a medium text" * 23, flavor=(2,))
        self.assertCannotEncode([12, 34])

    @with_flavor(0)
    def test_encoding(self):
        self.assertShouldEncodeSuccess("This is a small text", "kThis is a small text")
        self.assertShouldEncodeSuccess("This is a small text", "0kThis is a small text", flavor=(2,))
        self.assertShouldRaiseWhenEncoding("This is a medium text" * 13, ValueError)
        self.assertShouldEncodeSuccess("", "0")

    @with_flavor(2)
    def test_can_decode(self):
        self.assertCanDecode("kThis is a small text")
        self.assertCannotDecode(345453)
        self.assertCannotDecode("X")
        self.assertCannotDecode("XL")
        self.assertCanDecode("XXL")

    @with_flavor(1)
    def test_decode(self):
        self.assertShouldRaiseWhenDecoding("kThis is a small text", ValueError)
        self.assertShouldDecodeSuccess("kThis is a small text", "This is a small text", flavor=(1,))
        self.assertShouldDecodeSuccess("00", "")
        self.assertShouldRaiseWhenDecoding("0", (ValueError, AssertionError))

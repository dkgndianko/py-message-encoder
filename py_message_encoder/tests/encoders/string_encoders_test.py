from py_message_encoder.encoders.string_encoders import FixedLengthEncoder
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class FixedLengthEncoderTest(EncoderTest):
    ENCODER_CLASS = FixedLengthEncoder
    FLAVORS = [(1,), (2,), (3,)]

    @with_flavor(0)
    def test_encoding_to_one_char(self):
        self.assertShouldEncodeSuccess("3", "3")
        self.assertShouldEncodeSuccess("s", "s")
        self.assertShouldEncodeSuccess("", " ")

    @with_flavor(1)
    def test_encoding_to_two_char(self):
        self.assertShouldEncodeSuccess("3", " 3")
        self.assertShouldEncodeSuccess("se", "se")
        self.assertShouldEncodeSuccess("", "  ")

    @with_flavor(1)
    def test_encoding_non_string(self):
        self.assertShouldRaiseWhenEncoding(4, ValueError)
        self.assertShouldRaiseWhenEncoding(4.0, ValueError)
        self.assertShouldRaiseWhenEncoding([45, 23], ValueError)

    @with_flavor(2)
    def test_encode_decode_matching(self):
        self.assertShouldEncodeDecodeMatch("DK")

    @with_flavor(0)
    def test_decode_(self):
        self.assertShouldDecodeSuccess("D", "D")
        self.assertShouldDecodeSuccess(" AI", "AI", flavor=(3,))

from py_message_encoder.encoders.boolean_encoder import BooleanEncoder
from py_message_encoder.tests.encoder_test import EncoderTest


class BooleanEncoderTest(EncoderTest):
    ENCODER_CLASS = BooleanEncoder

    def test_encode_truthy(self):
        self.assertShouldEncodeSuccess(True, "1", "Failed encoding boolean True")
        self.assertShouldEncodeSuccess(56, "1", "Failed encoding truthy integer 56")
        self.assertShouldEncodeSuccess("abc", "1", "Failed encoding truthy string 'abc'")
        self.assertShouldEncodeSuccess([56, 34], "1", "Failed encoding truthy list '[56, 34]'")

    def test_encode_falsy(self):
        self.assertShouldEncodeSuccess(False, "0", "Failed encoding boolean False")
        self.assertShouldEncodeSuccess(0, "0", "Failed encoding falsy integer 0")
        self.assertShouldEncodeSuccess("", "0", "Failed encoding falsy empty string ''")
        self.assertShouldEncodeSuccess([], "0", "Failed encoding falsy empty list '[]'")

    def test_decode_true(self):
        self.assertShouldDecodeSuccess("1", True, "Cannot decode '1' to True")
        self.assertShouldDecodeSuccess("1X3534", True, "Cannot decode '1X3534' to True")

    def test_decode_false(self):
        self.assertShouldDecodeSuccess("0", False)
        self.assertShouldDecodeSuccess("0er34", False, "Cannot decode '0er34' to False")

    def test_can_decode(self):
        self.assertCanDecode("0", "Encoded boolean cannot be decoded")
        self.assertCanDecode("145fdrg", "Encoded boolean cannot be decoded")
        self.assertCannotDecode("", "Non encoded boolean value is decoded")
        self.assertCannotDecode("Drtt", "Non encoded boolean value is decoded")

from datetime import time

from py_message_encoder.encoders.date_encoders import TimeEncoder
from py_message_encoder.tests.encoder_test import EncoderTest


class TimeEncoderTest(EncoderTest):
    ENCODER_CLASS = TimeEncoder

    def test_can_encode(self):
        self.assertCannotEncode([34, 56])
        self.assertCanEncode(time(23, 59, 59))
        self.assertCannotEncode(time.fromisoformat("17:15:19+09:15"))

    def test_encode(self):
        self.assertShouldEncodeSuccess(time.fromisoformat("15:24:39"), "o36[D")
        self.assertShouldEncodeSuccess(time.fromisoformat("15:24:39+08:00"), "E36[D")
        self.assertShouldEncodeSuccess(time.fromisoformat("23:59:59+14:00"), "Q3aX<")
        self.assertShouldEncodeSuccess(time.fromisoformat("00:00:00-12:00"), "010")
        self.assertShouldRaiseWhenEncoding(time.fromisoformat("04:11:23-02:12"), ValueError)

    def test_can_decode(self):
        self.assertCanDecode("00")
        self.assertCanDecode("010")
        self.assertCanDecode("010")
        self.assertCanDecode("")

    def test_decode(self):
        self.assertShouldDecodeSuccess("x2Er", time.fromisoformat("01:00:27+04:30"))
        self.assertShouldRaiseWhenDecoding("", AssertionError)

    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch(time.fromisoformat("13:15:27+00:00"))
        self.assertShouldDecodeEncodeMismatch("00")

from datetime import datetime

from py_message_encoder.encoders.date_encoders import DateTimeEncoder
from py_message_encoder.tests.encoder_test import EncoderTest


class DateTimeEncoderTest(EncoderTest):
    ENCODER_CLASS = DateTimeEncoder

    def test_can_encode(self):
        self.assertCannotEncode([34, 56])
        self.assertCanEncode(datetime(1990, 8, 5))
        self.assertCannotEncode(datetime.fromisoformat("2021-12-28 17:15:19+09:15"))

    def test_encode(self):
        self.assertShouldEncodeSuccess(datetime.fromisoformat("2020-11-18 12:15:19+08:30"), "F5oGS(j")
        self.assertShouldEncodeSuccess(datetime.fromisoformat("2016-07-17 15:24:39+08:00"), "E5my*KD")
        self.assertShouldEncodeSuccess(datetime.fromisoformat("2016-07-17 23:59:59+14:00"), "Q5my+t<")
        self.assertShouldEncodeSuccess(datetime.fromisoformat("2016-07-17 00:00:00-12:00"), "05my!Y0")
        self.assertShouldRaiseWhenEncoding(datetime.fromisoformat("2016-07-17 04:11:23-02:12"), ValueError)

    def test_can_decode(self):
        self.assertCanDecode("00")
        self.assertCanDecode("010")
        self.assertCanDecode("010")
        self.assertCanDecode("")

    def test_decode(self):
        self.assertShouldDecodeSuccess("x2Er", datetime.fromisoformat("1970-01-01 01:00:27+04:30"))
        self.assertShouldRaiseWhenDecoding("", AssertionError)

    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch(datetime.fromisoformat("2016-07-17 13:15:27+00:00"))
        self.assertShouldDecodeEncodeMismatch("00")

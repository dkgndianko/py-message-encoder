from datetime import date, datetime

from py_message_encoder.encoders.date_encoders import DateEncoder
from py_message_encoder.tests.encoder_test import EncoderTest


class DateEncoderTest(EncoderTest):
    ENCODER_CLASS = DateEncoder

    CURRENT_FLAVOR = ()

    def test_can_encode(self):
        self.assertCanEncode(date.fromtimestamp(0))
        self.assertCannotEncode("2021-12-24")
        self.assertCanEncode(datetime.fromisoformat("2021-12-24 14:36:10"))

    def test_encode(self):
        self.assertShouldEncodeSuccess(date.fromisoformat("1990-07-28"), "2\\H")
        self.assertShouldEncodeSuccess(datetime.fromisoformat("2021-12-24 05:36:10"), "32u.")
        self.assertShouldEncodeSuccess(datetime.fromisoformat("2021-12-24 05:36:10-11:00"), "32u.")
        self.assertShouldEncodeSuccess(datetime.fromisoformat("9999-12-31 23:59:59.999999"), "4427%")

    def test_can_decode(self):
        self.assertCanDecode("2bagsofnuggets")
        self.assertCanDecode("3bagsofnuggets")

    def test_decode(self):
        self.assertShouldDecodeSuccess("2bags", date(1972, 9, 27))
        self.assertShouldDecodeSuccess("3bags", date(2216, 6, 16))
        self.assertShouldDecodeSuccess("3222", date(2014, 11, 8))
        self.assertShouldRaiseWhenDecoding("4bags", OverflowError)

    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch(date(1990, 7, 28))
        self.assertShouldEncodeDecodeMismatch(datetime(1990, 7, 28))
        self.assertShouldDecodeEncodeMatch("2??")
        self.assertShouldDecodeEncodeMismatch("20?")

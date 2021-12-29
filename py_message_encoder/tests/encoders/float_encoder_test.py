from py_message_encoder.encoders.float_encoders import FloatEncoder
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class FloatEncoderTest(EncoderTest):
    ENCODER_CLASS = FloatEncoder
    FLAVORS = [(0,), (4,), (6,), (10,), (15,)]

    def test_can_encode(self):
        self.assertCannotEncode(12)
        self.assertCanEncode(12.0)

    @with_flavor(3)
    def test_encode(self):
        self.assertShouldEncodeSuccess(3.14, "g23I")
        self.assertShouldEncodeSuccess(3.1415926535, "g65s-NEz")
        self.assertShouldEncodeSuccess(314159265.35, "o65s-NEz")
        self.assertShouldEncodeSuccess(0.0, "e10")

    @with_flavor(4)
    def test_encode_very_long_decimals(self):
        self.assertShouldEncodeSuccess(3.141592653589793, "g8$ZFG@hUR")
        self.assertShouldEncodeSuccess(0.0004153, "c2Kd")

    def test_can_decode(self):
        self.assertCanDecode("h390u")

    @with_flavor(2)
    def test_decode(self):
        self.assertShouldDecodeSuccess("h390u", 72.93)
        self.assertShouldDecodeSuccess("g86Pddos&X", 3.14159265358979)
        self.assertShouldDecodeSuccess("g8$ZFG@hUR", 3.141592653589793)
        self.assertShouldDecodeSuccess("t234", 274.0)
        self.assertShouldRaiseWhenDecoding("g9$ZFG@hUR", ValueError)

    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch(23.091234)
        self.assertShouldEncodeDecodeMatch(0.091234)
        self.assertShouldEncodeDecodeMatch(0.000934)
        self.assertShouldDecodeEncodeMatch("i234")

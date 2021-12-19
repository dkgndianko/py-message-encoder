from py_message_encoder.encoders.integer_encoders import IntFixedLengthEncoder, \
    _IntFixedLengthEncoder
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class _IntFixedLengthEncoderTest(EncoderTest):
    ENCODER_CLASS = _IntFixedLengthEncoder
    FLAVORS = [(5,), (10,)]

    @with_flavor(0)
    def test_can_encode(self):
        self.assertCannotEncode(674821)
        self.assertCanEncode(674821, flavor=(7,))
        self.assertCanEncode(89873)
        self.assertCannotEncode(-89873)
        self.assertCanEncode(-8987)
        self.assertCannotEncode(3.14)
        self.assertCannotEncode("24")
        self.assertCannotEncode([12, 34])

    @with_flavor(1)
    def test_encode(self):
        self.assertShouldEncodeSuccess(20211219, "0020211219")
        self.assertShouldEncodeSuccess(2021121914, "2021121914")
        self.assertShouldRaiseWhenEncoding(349829, ValueError, flavor=(4,))
        self.assertShouldEncodeSuccess(-5032390, "00-5032390")

    @with_flavor(0)
    def test_can_decode(self):
        self.assertCanDecode("00298878t12")
        self.assertCanDecode("00298878t")
        self.assertCannotDecode("0029")
        self.assertCannotDecode(20934)

    @with_flavor(1)
    def test_decode(self):
        self.assertShouldDecodeSuccess("0003049030", 3049030)
        self.assertShouldRaiseWhenDecoding("0003049", (ValueError, AssertionError))
        self.assertShouldDecodeSuccess("00-5032390", -5032390)
        self.assertShouldDecodeSuccess("0005032390", 5032390)
        self.assertShouldDecodeSuccess("-503239048", -503239048)
        self.assertShouldFailDecoding("-5032390484", -5032390484)

    @with_flavor(1)
    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch(1921681)
        self.assertShouldDecodeEncodeMismatch("-000304526")
        self.assertShouldDecodeEncodeMismatch("00-0304526")
        self.assertShouldDecodeEncodeMatch("000-304526")


class IntFixedLengthEncoderTest(EncoderTest):
    ENCODER_CLASS = IntFixedLengthEncoder
    FLAVORS = [(3,), (5,)]

    @with_flavor(0)
    def test_can_encode(self):
        self.assertCanEncode(674821)  # 720899
        self.assertCanEncode(89873)
        self.assertCanEncode(-89873)
        self.assertCannotEncode(3.14)
        self.assertCannotEncode("24")
        self.assertCannotEncode([12, 34])
        self.assertCanEncode(5839289999, flavor=(5,))
        self.assertCannotEncode(58392810000, flavor=(5,))

    @with_flavor(1)
    def test_encode(self):
        self.assertShouldEncodeSuccess(20211219, "0r$j9")
        self.assertShouldEncodeSuccess(5839289999, "><<<<")
        self.assertShouldEncodeSuccess(2021121914, "u_Fke")
        self.assertShouldEncodeSuccess(-5032390, "<6'pE")
        self.assertShouldEncodeSuccess(-5032390, "00000<6'pE", flavor=(10,))
        self.assertShouldRaiseWhenEncoding(58392810000, ValueError)

    @with_flavor(0)
    def test_can_decode(self):
        self.assertCanDecode("000")
        self.assertCannotDecode("00")
        self.assertCannotDecode([45, 45])

    @with_flavor(1)
    def test_decode(self):
        self.assertShouldDecodeSuccess("Cidem", 2506408582)
        self.assertShouldDecodeSuccess("Cidemia", 2506408582)
        self.assertShouldDecodeSuccess("Cidemia", 20301909515830, flavor=(7,))
        self.assertShouldFailDecoding("10001", 10001)
        self.assertShouldRaiseWhenDecoding("VDN|A", ValueError)

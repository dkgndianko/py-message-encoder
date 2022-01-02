from py_message_encoder.encoders.integer_encoders import big_int, unsigned_small_int
from py_message_encoder.encoders.list_encoders import HomogenousListEncoder
from py_message_encoder.encoders.message_body_encoder import BodyEncoder, FieldMapping, MessageField
from py_message_encoder.encoders.string_encoders import LLVAR, LVAR
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class HomogenousListEncoderTest(EncoderTest):
    ENCODER_CLASS = HomogenousListEncoder

    a_body_encoder = BodyEncoder(FieldMapping([MessageField(n, LVAR) for n in ["first", "second"]]))
    FLAVORS = [(big_int, ), (LLVAR, ), (a_body_encoder,), (unsigned_small_int, )]

    @with_flavor(0)
    def test_can_encode(self):
        self.assertCanEncode([])
        self.assertCanEncode([1, 2, 3])
        self.assertCannotEncode((1, 2, 4))
        self.assertCannotEncode((x+1 for x in range(10)))
        self.assertCanEncode(list(x+1 for x in range(10)))
        self.assertCannotEncode("This is a str!")

    @with_flavor(0)
    def test_encode(self):
        self.assertShouldEncodeSuccess([10, 9, 8, 7], "141a191817")
        self.assertShouldRaiseWhenEncoding(["This", "is", "dope"], ValueError)
        self.assertShouldEncodeSuccess(["This", "is", "dope"], "134This2is4dope", flavor=(LVAR,))
        self.assertShouldEncodeSuccess([{"first": "DKG", "second": "Cidemia"}, {"first": "Break", "second": "Rebuild"}],
                                       "12022<13DKG7Cidemia022<15Break7Rebuild", flavor=2)

    @with_flavor(1)
    def test_can_decode(self):
        self.assertCanDecode("00")

    @with_flavor(1)
    def test_decode(self):
        self.assertShouldDecodeSuccess("10", [])
        self.assertShouldDecodeSuccess("1203DKG07Cidemia", ['DKG', 'Cidemia'])
        self.assertShouldDecodeSuccess("123DKG7Cidemia", ['DKG', 'Cidemia'], flavor=(LVAR,))
        self.assertShouldDecodeSuccess("123DKG7Cidemia", [320082, 20301909515830], flavor=0)
        self.assertShouldRaiseWhenDecoding("1804XBEE", ValueError)

    @with_flavor(1)
    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch([])
        self.assertShouldDecodeEncodeMatch('1h050c0j0q0x0E0L0S0Z0&0=0"0<161d1k1r', flavor=3)

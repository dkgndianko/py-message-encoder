from py_message_encoder.encoders.integer_encoders import IntegerVarLengthEncoder
from py_message_encoder.tests.encoder_test import EncoderTest, with_flavor


class IntegerVariableLengthEncoderTest(EncoderTest):
    ENCODER_CLASS = IntegerVarLengthEncoder
    FLAVORS = [(1,), (2,)]

    def setUp(self) -> None:
        # 312889237899995279559543569011991444563032149898984512724063393645184626460424889060216384195510981201000000000000000000000000000000000000000000000000000000000000
        self.big_number = 58392810000 ** 15
        self.very_big_number = 58392810000 ** 25

    @with_flavor(0)
    def test_can_encode(self):
        self.assertCanEncode(58392810000)
        self.assertCannotEncode(1.09)
        self.assertCanEncode(self.big_number)
        self.assertCannotEncode(self.very_big_number)
        self.assertCanEncode(self.very_big_number, flavor=(2,))

    @with_flavor(0)
    def test_encode(self):
        self.assertShouldEncodeSuccess(893432490234902342342390, "d3e@zB?tg5nfHk")
        self.assertShouldEncodeSuccess(self.big_number, "\\hZpEEYS4s_*/L$rGr1r<$^;blWUpp{cB[8{]WesV{rF9qZdxD_k&wXj98SANEw<W@+i;000000000000000")
        self.assertShouldRaiseWhenEncoding(self.very_big_number, ValueError)
        self.assertShouldEncodeSuccess(self.very_big_number, "1Mq*\\2.Jxlw;0IFpk9G57tD;MRi>%I#uw{H\">$C<kAK/vQMx9N4v@HE.7<(2WE7GpYH@s,]$LJ,Q%NcgzfP5Vr7}\"uo3;4'PLPTOb\\f(=wF#;_;;9{;0000000000000000000000000", flavor=(2,))
        self.assertShouldEncodeSuccess(600, "26Y")
        self.assertShouldEncodeSuccess(-600, "3<6Y")
        self.assertShouldEncodeSuccess(0, "10")

    @with_flavor(0)
    def test_can_decode(self):
        self.assertCanDecode("dfeklnfwoiefwhef")
        self.assertCannotDecode("")
        self.assertCanDecode("X")

    @with_flavor(0)
    def test_decode(self):
        self.assertShouldDecodeSuccess("dfeklnfwoiefwhef", 4281082123120121670910397)
        self.assertShouldDecodeSuccess("dfeklnfwoiefwh", 4281082123120121670910397)
        self.assertShouldRaiseWhenDecoding("dfeklnfwoiefw", ValueError)
        self.assertShouldDecodeSuccess("0", 0)

    @with_flavor(0)
    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch(100)
        self.assertShouldDecodeEncodeMatch("akhiefsesdg")
        self.assertShouldDecodeEncodeMismatch("a0hiefsesdg")

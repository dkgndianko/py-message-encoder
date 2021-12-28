from py_message_encoder.encoders.message_header_encoder import MessageHeaderEncoder
from py_message_encoder.header import MessageHeader
from py_message_encoder.tests.encoder_test import EncoderTest


class MessageHeaderEncoderTest(EncoderTest):
    ENCODER_CLASS = MessageHeaderEncoder

    def test_can_encode(self):
        self.assertCanEncode(MessageHeader(12))
        self.assertCannotEncode("this is a string")
        self.assertCannotEncode(8268)
        self.assertCannotEncode(8268)
        self.assertCannotEncode(MessageHeader(9999))

    def test_encode(self):
        self.assertShouldEncodeSuccess(MessageHeader(6), "0610")
        self.assertShouldEncodeSuccess(MessageHeader(6).set_presence(5, True), "0611")
        self.assertShouldEncodeSuccess(MessageHeader(6).set_presence(3, True), "0614")
        h = MessageHeader(6)
        for i in range(h.number_of_parts):
            h.set_presence(i, True)
        self.assertShouldEncodeSuccess(h, "062<v")
        h2 = MessageHeader(112)
        for i in range(3, h2.number_of_parts, 7):
            h2.set_presence(i, True)
        self.assertShouldEncodeSuccess(h2, "1mhhWP}_d\\LaY@aS^c.u")
        self.assertShouldRaiseWhenEncoding(MessageHeader(10000), ValueError)

    def test_can_decode(self):
        self.assertCanDecode("162<v")
        self.assertCannotDecode("16")

    def test_decode(self):
        h = MessageHeader(15)
        for p in [3, 5, 6, 7, 10, 11, 12, 14]:
            h.set_presence(p, True)
        self.assertShouldDecodeSuccess("0f2x3", h)
        self.assertShouldDecodeSuccess("0211", MessageHeader(2).set_presence(1))

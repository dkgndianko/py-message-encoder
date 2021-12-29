from datetime import date, datetime, time, timezone, timedelta

from py_message_encoder.body import MessageBody
from py_message_encoder.encoders.boolean_encoder import BooleanEncoder
from py_message_encoder.encoders.date_encoders import DateEncoder, DateTimeEncoder, TimeEncoder
from py_message_encoder.encoders.integer_encoders import UnsignedIntFixedLengthEncoder, IntegerVarLengthEncoder
from py_message_encoder.encoders.message_body_encoder import BodyEncoder, MessageField, FieldMapping
from py_message_encoder.encoders.string_encoders import LVAR, FixedLengthEncoder
from py_message_encoder.tests.encoder_test import EncoderTest


class BodyEncoderTest(EncoderTest):
    ENCODER_CLASS = BodyEncoder

    def setUp(self) -> None:
        mapping = [
            ("internal_id", FixedLengthEncoder(7)),
            ("first_name", LVAR),
            ("last_name", LVAR),
            ("date_of_birth", DateEncoder()),
            ("grade", UnsignedIntFixedLengthEncoder(2)),
            ("joined_at", DateTimeEncoder()),
            ("day_start", TimeEncoder()),
            ("pending_points", IntegerVarLengthEncoder()),
            ("activated", BooleanEncoder()),
        ]
        self.field_mapping = FieldMapping([MessageField(name, encoder) for name, encoder in mapping])
        self.field_names = [name for name, _ in mapping]
        self.body = MessageBody(self.field_names)
        type(self).CURRENT_FLAVOR = (self.field_mapping,)

    def test_can_encode(self):
        self.assertCanEncode(self.body)
        self.assertCannotEncode(10.2)

    def test_encode(self):
        data = {"first_name": "Xorom", "last_name": "Polle", "joined_at": datetime(2021, 12, 29, 14, 24, 11),
                "grade": 12, "activated": True, "pending_points": 98234, "internal_id": "LCX0492"}
        self.body.update(data)
        self.assertShouldEncodeSuccess(self.body, "093<2DLCX04925Xorom5Polle0co5p0%Ab3cbI1")
        self.body.update({"first_name": None})
        self.assertShouldEncodeSuccess(self.body, "093<11LCX04925Polle0co5p0%Ab3cbI1")
        self.body.update({
            "first_name": "Fass-katu", "last_name": "Laax", "day_start": time.fromisoformat("08:30:00-04:30"),
            "date_of_birth": date(2014, 5, 11), "internal_id": "DKG05"
        })
        self.assertShouldEncodeSuccess(self.body, "093<2=  DKG059Fass-katu4Laax32010co5p0%Abf33(03cbI1")
        self.assertShouldRaiseWhenEncoding({"unknown_field": 500}, KeyError)

    def test_can_decode(self):
        self.assertCannotDecode("RT")
        self.assertCanDecode("RT00PxDude")

    def test_decode(self):
        self.assertShouldDecodeSuccess("0922c5Xorom5Polle", {"first_name": "Xorom", "last_name": "Polle"})
        self.assertShouldRaiseWhenDecoding("093<2D5Xorom5Polle", ValueError)
        expected = {'internal_id': 'DKG05', 'first_name': 'Fass-katu', 'last_name': 'Laax',
                    'date_of_birth': date(2014, 5, 11), 'grade': 12, 'pending_points': 98234,
                    'joined_at': datetime(2021, 12, 29, 14, 24, 11, tzinfo=timezone.utc), 'activated': True,
                    'day_start': time(8, 30, 0, tzinfo=timezone(timedelta(days=-1, seconds=70200)))}
        self.assertShouldDecodeSuccess("093<2=  DKG059Fass-katu4Laax32010co5p0%Abf33(03cbI1", expected)
        expected = {'internal_id': 'JuddTay', 'first_name': 'Samba', 'last_name': 'Neeg',
                    'date_of_birth': date(2021, 12, 29), 'activated': False}
        self.assertShouldDecodeSuccess("093<2JJuddTay5Samba4Neeg32v00", expected)

    def test_encode_decode(self):
        self.assertShouldEncodeDecodeMatch({"first_name": "Samba", "last_name": "Neeg", "date_of_birth": date.today()})
        self.assertShouldEncodeDecodeMismatch({"first_name": None, "last_name": "Neeg"})
        self.assertShouldDecodeEncodeMatch("093<2JJuddTay5Samba4Neeg32v00")

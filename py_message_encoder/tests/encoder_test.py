from typing import Any, List, Tuple
from unittest import TestCase

from py_message_encoder.encoders import PartialEncoder


class EncoderTest(TestCase):
    ENCODER_CLASS = None
    FLAVORS: List[Tuple] = []  # list of different argument cases to pass to the __init__ method of the encoder class
    CURRENT_FLAVOR = ()

    @classmethod
    def __get_instance_with_flavor(cls, flavor=None):
        if hasattr(cls, 'INSTANCES') is False:
            cls.INSTANCES = {}
        if flavor is None:
            flavor = cls.CURRENT_FLAVOR
        _flavor = hash(flavor)
        try:
            instance = cls.INSTANCES[_flavor]
        except KeyError:
            instance = cls.ENCODER_CLASS(*flavor)
            cls.INSTANCES[_flavor] = instance
        return instance

    def get_encoder(self, flavor=None) -> PartialEncoder:
        return self.__get_instance_with_flavor(flavor)

    def assertShouldEncodeSuccess(self, payload: Any, expected: str, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        encoded = instance.encode(payload)
        self.assertEqual(encoded, expected, message or f"Failing encoding {instance.message_type} '{payload}' to "
                                                       f"'{expected}'")

    def assertShouldDecodeSuccess(self, payload: str, expected: Any, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        decoded, _ = instance.decode(payload)
        self.assertEqual(decoded, expected, message or f"Cannot decode '{payload}' to {instance.message_type} {expected}")

    def assertShouldEncodeDecodeMatch(self, payload: Any, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        encoded = instance.encode(payload)
        decoded, consumed = instance.decode(encoded)
        self.assertEqual(decoded, payload, message or "Encode -> Decode not giving the same value")

    def assertShouldFailEncoding(self, payload: Any, unexpected: Any, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        encoded = instance.encode(payload)
        self.assertNotEqual(encoded, unexpected, message or f"Not expected to encode {instance.message_type} '{payload}"
                                                            f"' to '{unexpected}'")

    def assertShouldFailDecoding(self, payload: str, unexpected: Any, message: str = None, flavor=None):
        decoded, _ = self.get_encoder(flavor).decode(payload)
        self.assertNotEqual(decoded, unexpected, message or f"Not expected to decode '{payload}' to {unexpected}")

    def _can_decode(self, value: Any, flavor=None) -> bool:
        try:
            can = self.get_encoder(flavor).can_decode(value)
        except AssertionError:
            can = False
        return can

    def _can_encode(self, value: Any, flavor=None) -> bool:
        can, me = self.get_encoder(flavor).can_encode(value)
        print(f"me: {me}")
        return can

    def assertCanEncode(self, value: Any, message: str = None, flavor=None):
        self.assertTrue(self._can_encode(value, flavor), message or "Expecting to be able to encode the value")

    def assertCannotEncode(self, value: Any, message: str = None, flavor=None):
        self.assertFalse(self._can_encode(value, flavor), message or "Expecting to not be able to encode the value")

    def assertCanDecode(self, value: Any, message: str = None, flavor=None):
        self.assertTrue(self._can_decode(value, flavor), message or "Expecting to be able to decode the value")

    def assertCannotDecode(self, value: Any, message: str = None, flavor=None):
        self.assertFalse(self._can_decode(value, flavor), message or "Expecting to not be able to decode the value")

    def assertShouldEncodeDecodeMismatch(self, payload: Any, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        encoded = instance.encode(payload)
        decoded, consumed = instance.decode(encoded)
        self.assertNotEqual(decoded, payload, message or "Encode -> Decode not expected to give the same value")

    def assertShouldDecodeEncodeMatch(self, value: str, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        decoded, _ = instance.decode(value)
        encoded = instance.encode(decoded)
        self.assertEqual(encoded, value, message or "Decode -> Encode not giving the same value")

    def assertShouldDecodeEncodeMismatch(self, value: str, message: str = None, flavor=None):
        instance = self.get_encoder(flavor)
        decoded, _ = instance.decode(value)
        encoded = instance.encode(decoded)
        self.assertNotEqual(encoded, value, message or "Decode -> Encode not expected to give the same value")

    def assertShouldRaiseWhenEncoding(self, value: Any, expected_exception, message: str = None, flavor=None):
        with self.assertRaises(expected_exception, msg=message):
            self.get_encoder(flavor).encode(value)

    def assertShouldRaiseWhenDecoding(self, payload: str, expected_exception, message: str = None, flavor=None):
        with self.assertRaises(expected_exception, msg=message):
            self.get_encoder(flavor).decode(payload)


def with_flavor(flavor: int):
    def annotation(method):

        def new_method(self: EncoderTest):
            clazz = type(self)
            flavor_backup = clazz.CURRENT_FLAVOR
            try:
                clazz.CURRENT_FLAVOR = clazz.FLAVORS[flavor]
            except IndexError:
                raise ValueError(f"Not such flavor at index {flavor}")
            try:
                method(self)
            finally:
                clazz.CURRENT_FLAVOR = flavor_backup

        return new_method

    return annotation

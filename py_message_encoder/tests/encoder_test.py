from typing import Any, List, Tuple
from unittest import TestCase

from py_message_encoder.encoders import PartialEncoder


class EncoderTest(TestCase):
    ENCODER_CLASS = None
    FLAVORS: List[Tuple] = []  # list of different argument cases to pass to the __init__ method of the encoder class
    __INSTANCES = {}
    CURRENT_FLAVOR = ()

    def __get_instance_with_flavor(self, flavor=None):
        if flavor is None:
            flavor = self.CURRENT_FLAVOR
        _flavor = hash(flavor)
        try:
            instance = self.__INSTANCES[_flavor]
        except KeyError:
            instance = self.ENCODER_CLASS(*flavor)
            self.__INSTANCES[_flavor] = instance
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

    def assertShouldEncodeDecodeMatch(self):
        pass

    def assertShouldFailEncoding(self, payload: str, unexpected: Any, message: str, flavor=None):
        instance = self.get_encoder(flavor)
        encoded = instance.encode(payload)
        self.assertNotEqual(encoded, unexpected, message or f"Not expected to encode {instance.message_type} '{payload}"
                                                            f"' to '{unexpected}'")

    def assertShouldFailDecoding(self, payload: str, unexpected: Any, message: str, flavor=None):
        decoded, _ = self.get_encoder(flavor).decode(payload)
        self.assertNotEqual(decoded, unexpected, message or f"Not expected to decode '{payload}' to {unexpected}")

    def _can_decode(self, value: Any, flavor=None) -> bool:
        try:
            can = self.get_encoder(flavor).can_decode(value)
        except AssertionError:
            can = False
        return can

    def assertCanDecode(self, value: Any, message: str, flavor=None):
        self.assertTrue(self._can_decode(value, flavor), message)

    def assertCannotDecode(self, value: Any, message: str, flavor=None):
        self.assertFalse(self._can_decode(value, flavor), message)

    def assertShouldEncodeDecodeMismatch(self, value: Any, message: str, flavor=None):
        pass

    def assertShouldRaiseWhenEncoding(self, value: Any, expected_exception, message: str = None, flavor=None):
        with self.assertRaises(expected_exception, msg=message):
            self.get_encoder(flavor).encode(value)

    def assertShouldRaiseDecoding(self, payload: str, message: str, flavor=None):
        pass


def with_flavor(flavor: int):
    def annotation(method):

        def new_method(self: EncoderTest):
            flavor_backup = self.CURRENT_FLAVOR
            try:
                self.CURRENT_FLAVOR = self.FLAVORS[flavor]
            except IndexError:
                raise ValueError(f"Not such flavor at index {flavor}")
            try:
                method(self)
            finally:
                self.CURRENT_FLAVOR = flavor_backup

        return new_method

    return annotation

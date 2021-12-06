from typing import Any
from unittest import TestCase

from py_message_encoder.encoders import PartialEncoder


class EncoderTest(TestCase):
    ENCODER_CLASS = None
    FLAVORS = []
    __INSTANCES = {}

    def __get_instance_with_flavor(self, flavor=()):
        _flavor = hash(flavor)
        try:
            instance = self.__INSTANCES[_flavor]
        except KeyError:
            instance = self.ENCODER_CLASS(*flavor)
            self.__INSTANCES[_flavor] = instance
        return instance

    def get_encoder(self, flavor=()) -> PartialEncoder:
        return self.__get_instance_with_flavor(flavor)

    def assertShouldEncodeSuccess(self, payload: Any, expected: str, message: str = None, flavor=()):
        instance = self.get_encoder(flavor)
        encoded = instance.encode(payload)
        self.assertEqual(encoded, expected, message or f"Failing encoding {instance.message_type} '{payload}' to "
                                                       f"{expected}")

    def assertShouldDecodeSuccess(self, payload: str, expected: Any, message: str = None, flavor=()):
        instance = self.get_encoder(flavor)
        decoded, _ = instance.decode(payload)
        self.assertEqual(decoded, expected, message or f"Cannot decode '{payload}' to {instance.message_type} {expected}")

    def assertShouldEncodeDecodeMatch(self):
        pass

    def assertShouldFailEncoding(self, payload: str, unexpected: Any, message: str, flavor=()):
        pass

    def assertShouldFailDecoding(self, payload: str, unexpected: Any, message: str, flavor=()):
        decoded, _ = self.get_encoder(flavor).decode(payload)
        print(f"decoded: {decoded}")
        self.assertNotEqual(decoded, decoded, message)

    def _can_decode(self, value: Any, flavor=()) -> bool:
        try:
            can = self.get_encoder(flavor).can_decode(value)
        except AssertionError:
            can = False
        return can

    def assertCanDecode(self, value: Any, message: str, flavor=()):
        self.assertTrue(self._can_decode(value, flavor), message)

    def assertCannotDecode(self, value: Any, message: str, flavor=()):
        self.assertFalse(self._can_decode(value, flavor), message)

    def assertShouldEncodeDecodeMismatch(self):
        pass

    def assertShouldRaiseEncoding(self):
        pass

    def assertShouldRaiseDecoding(self):
        pass

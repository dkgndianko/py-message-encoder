from unittest import TestCase


class EncoderTest(TestCase):
    ENCODER_CLASS = None
    FLAVORS = []

    def __get_instance_with_flavor(self, flavor=()):
        return self.ENCODER_CLASS(**flavor)

    def should_fail_encoding(self, flavor=()):
        pass

    def should_fail_decoding(self, flavor=()):
        pass

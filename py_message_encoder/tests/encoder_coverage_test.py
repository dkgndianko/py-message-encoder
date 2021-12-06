import inspect
from unittest import TestCase

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.tests.encoder_test import EncoderTest
from py_message_encoder.tests.utils import get_objects_by_condition


def get_encoder_classes():
    return get_objects_by_condition(["py_message_encoder.encoders"], _is_encoder_sub_class)


def get_tested_encoders():
    test_classes = get_objects_by_condition(["py_message_encoder.encoders", "py_message_encoder.tests"],
                                            _is_encoder_test_class)
    return {t.ENCODER_CLASS for t in test_classes}


def _is_encoder_sub_class(t):
    return inspect.isclass(t) and issubclass(t, PartialEncoder) and t is not PartialEncoder


def _is_encoder_test_class(t):
    return inspect.isclass(t) and issubclass(t, EncoderTest) and t is not EncoderTest


EXCLUDED_ENCODERS = [

]


def is_not_excluded(t):
    return t not in EXCLUDED_ENCODERS


class TestEncoderTypeCoverage(TestCase):

    def test__encoder_type_coverage(self):
        all_encoders = get_encoder_classes()
        all_encoders = {t for t in all_encoders if is_not_excluded(t)}
        tested_encoders = get_tested_encoders()
        uncovered_encoders = all_encoders - tested_encoders
        if uncovered_encoders:
            absolute_classes = '\n'.join(sorted(f"{t.__module__}.{t.__name__}" for t in uncovered_encoders))
            raise Exception(f"There are Encoder classes without tests: {len(uncovered_encoders)}\n{absolute_classes}")

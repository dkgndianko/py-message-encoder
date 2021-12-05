import inspect
import pkgutil
from importlib import import_module
from typing import List
from unittest import TestCase

from py_message_encoder.encoders import PartialEncoder
from py_message_encoder.tests.encoder_test import EncoderTest


def get_objects_by_condition(root_packages: List[str], condition) -> set:
    res = set()
    for root_package in root_packages:
        pkg = import_module(root_package)
        for file_finder, name, is_pkg in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__package__ + '.'):
            for member_name, member in inspect.getmembers(import_module(name), condition):
                res.add(member)
    return res


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
    t not in EXCLUDED_ENCODERS


class TestEncoderTypeCoverage(TestCase):

    def test__encoder_type_coverage(self):
        all_encoders = get_encoder_classes()
        tested_encoders = get_tested_encoders()
        uncovered_encoders = all_encoders - tested_encoders
        if uncovered_encoders:
            absolute_classes = '\n'.join(sorted(f"{t.__module__}.{t.__name__}" for t in uncovered_encoders))
            raise Exception(f"There are Encoder classes without tests: {len(uncovered_encoders)}\n{absolute_classes}")


import inspect
import pkgutil
from importlib import import_module
from typing import List


def get_objects_by_condition(root_packages: List[str], condition) -> set:
    res = set()
    for root_package in root_packages:
        pkg = import_module(root_package)
        for file_finder, name, is_pkg in pkgutil.walk_packages(pkg.__path__, prefix=pkg.__package__ + '.'):
            for member_name, member in inspect.getmembers(import_module(name), condition):
                res.add(member)
    return res

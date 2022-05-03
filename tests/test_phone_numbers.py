import doctest
import unittest

from mw_commons import phone_numbers

# TODO: Add Comprehensive test suite in addition to the doctests

def load_tests(_loader, tests, _ignore):
    tests.addTests(doctest.DocTestSuite(phone_numbers))

    return tests
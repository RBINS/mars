"""
Launching all doctests in the tests directory using:

    - The test_suite helper from the testing product
    - the base layer in layer.py

"""

from mars.policy.tests.base import FunctionalTestCase
from mars.testing.tests.test_doctests import test_doctests_suite

################################################################################
# GLOBALS avalaible in doctests
# IMPORT/DEFINE objects there or inside ./user_globals.py (better)
# globals from the testing product are also available.
################################################################################
# example:
# from for import bar
# and in your doctests, you can do:
# >>> bar.something
from mars.policy.tests.globals import *
from mars.policy.tests import base
################################################################################

def test_suite():
    """."""
    return test_doctests_suite(
        __file__,
        globs=globals(),
        testklass=base.FunctionalTestCase
    )

# vim:set ft=python:

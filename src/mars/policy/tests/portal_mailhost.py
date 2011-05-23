# -*- coding: utf-8 -*-
"""
Asserts portal mailhost equal as in profile
"""

import os
import unittest
import logging

from Products.CMFCore.utils import getToolByName

from mars.policy.tests_tools import getMailHost
from mars.policy.tests.globals import (
    getTestingOptionsFromIni,
    errprint,
    ZOPETESTCASE,
    format_test_title,
)

_options = getTestingOptionsFromIni()
FAILS_ON_UNTESTED_ELEMENT = _options['FAILS_ON_UNTESTED_ELEMENT']
TEST_VERBOSE_MODE =  _options['TEST_VERBOSE_MODE']
TEST_SEQUENCE_TITLE = format_test_title('Checking Portal MailHost')

class CheckMailHost(unittest.TestCase):
    """."""

    def __init__(self, context, element, xml_policy=None):
        unittest.TestCase.__init__(self)
        self.context = context
        self.element = element

        if xml_policy:
            self.policy = getMailHost(xml_policy)
        else:
            # get default file in getMailhst : profile/default/mailhost.xml
            self.policy = getMailHost()

    def runTest(self):
        """."""

        mailhost = getToolByName(self.context, 'MailHost')
        info = ''

        if self.element[0] in self.policy:
            info = 'testing %s from policy' % self.element[0]
            self.assertEquals(
                self.policy[self.element[0]], getattr(mailhost, self.element[0]),
                msg = '%s founded in policy : %r != %r"' % (
                    self.element[0],
                    self.policy[self.element[0]],
                    getattr(mailhost, self.element[0])
                )
            )
        else:
            info = 'testing %s from default' % self.element[0]
            self.assertEquals(
                self.element[1], getattr(mailhost, self.element[0]),
                msg = "%s founded in default : %r != %r" % (
                    self.element[0],
                    self.element[1],
                    getattr(mailhost, self.element[0]
                           )
                )
            )
        if ZOPETESTCASE:
            if TEST_VERBOSE_MODE:
                errprint('\n'+info+'\n')
        else:
            logging.getLogger('Test mailhost').info(info)


def check_portal_mailhost(portal, xml_policy=None):
    """Return portal properties suite."""

    defaults = {
        'smtp_host': '',
        'smtp_port': 25,
        'smtp_userid': None,
        'smtp_pass': None,
        'smtp_notls': False
    }
    suite = unittest.TestSuite()

    if ZOPETESTCASE:
        if TEST_VERBOSE_MODE:
            errprint(TEST_SEQUENCE_TITLE)
        for property in defaults.iteritems():
            suite.addTest(CheckMailHost(portal, property))
        return suite
    else:
        logging.getLogger('Test mailhost').info(TEST_SEQUENCE_TITLE)
        res = unittest.TestResult()
        for property in defaults.iteritems():
            suite.addTest(CheckMailHost(portal, property))
        suite.run(res)
        return res.errors, res.failures

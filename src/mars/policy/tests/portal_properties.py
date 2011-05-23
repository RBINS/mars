# -*- coding: utf-8 -*-
"""
Asserts portal properties equal as in profile
"""

import os
import sys
import logging
import unittest

from mars.policy.tests_tools import getSiteProperties
from mars.policy.tests.globals import (
    getTestingOptionsFromIni,
    errprint,
    ZOPETESTCASE,
    format_test_title,
)



_options = getTestingOptionsFromIni()
FAILS_ON_UNTESTED_ELEMENT = _options['FAILS_ON_UNTESTED_ELEMENT']
TEST_VERBOSE_MODE =  _options['TEST_VERBOSE_MODE']
TEST_SEQUENCE_TITLE = format_test_title(' Checking Portal Properties')


def get_xml_default():
    from Products import CMFDefault
    return os.path.join(
        os.path.dirname(CMFDefault.__file__),
        'profiles', 'default', 'properties.xml'
    )

def get_xml_plone():
    from Products import CMFPlone
    return os.path.join(
        os.path.dirname(CMFPlone.__file__),
        'profiles', 'default', 'properties.xml'
    )

class BaseCheckProperties(unittest.TestCase):
    """Base class"""

    def __init__(self, context, element, xml_policy=None, xml_default=None, xml_plone=None):
        unittest.TestCase.__init__(self)
        if not xml_default: xml_default = get_xml_default()
        if not xml_plone: xml_plone = get_xml_plone()
        self.context = context
        self.element = element

        if xml_policy:
            self.policy = getSiteProperties(xml_policy)
        else:
            # get default file in getSiteProperties :
            # profile/default/properties.xml
            self.policy = getSiteProperties() 

        self.default = getSiteProperties(xml_default)
        self.plone = getSiteProperties(xml_plone)

    def runTest(self):
        """."""
        info = ''

        if self.element in self.policy:
            info = 'testing "%s" from policy' % self.element
            self.assertEquals(
                self.policy[self.element], self.context.getProperty(self.element),
                msg = 'Property "%s" founded in policy %r != %r' % (
                    self.element, self.policy[self.element],
                    self.context.getProperty(self.element)
                )
            )
        elif self.element in self.plone:
            info ='testing "%s" from cmfplone' % self.element
            self.assertEquals(
                self.plone[self.element], self.context.getProperty(self.element),
                msg = 'Property "%s" founded in CMFPlone %r != %r' % (
                    self.element,
                    self.plone[self.element],
                    self.context.getProperty(self.element)
                )
            )
        elif self.element in self.default:
            info ='testing "%s" from default' % self.element
            self.assertEquals(
                self.default[self.element], self.context.getProperty(self.element),
                msg = 'Property "%s" founded in CMFDefault %r != %r' % (
                    self.element,
                    self.default[self.element],
                    self.context.getProperty(self.element)
                )
            )
        else:
            info = '*** Warning *** "%s" is not tested, not founded' \
                   ' in policy or CMFdefault' % self.element
            if ZOPETESTCASE:
                if not FAILS_ON_UNTESTED_ELEMENT:
                    errprint('\n'+info+'\n')
                    return
            self.fail(msg=info)

        if ZOPETESTCASE:
            if TEST_VERBOSE_MODE:
                errprint('\n'+info+'\n')
        else:
            logging.getLogger('Test properties').info(info)

def check_portal_properties(portal, xml_policy=None, xml_default=None):
    """Return portal properties suite."""
    suite = unittest.TestSuite()

    if ZOPETESTCASE:
        if TEST_VERBOSE_MODE:
            errprint(TEST_SEQUENCE_TITLE)
        for property in portal.propertyIds():
            suite.addTest(BaseCheckProperties(portal, property))
        return suite
    else:
        logging.getLogger('Test Properties').info(TEST_SEQUENCE_TITLE)
        res = unittest.TestResult()
        for property in portal.propertyIds():
            suite.addTest(BaseCheckProperties(portal, property))
        suite.run(res)
        return res.errors, res.failures

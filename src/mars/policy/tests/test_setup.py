"""
Checking specifics portal settings.
This package must run in a policy package (needs app_config.py)
"""
import unittest

from Products.CMFCore.utils import getToolByName

from mars.policy.app_config import SKIN, PRODUCT_DEPENDENCIES, GLOBALS
from mars.policy.tests_tools import getWorkflows
from mars.policy.tests.base import TestCase, setup_site
from mars.policy.tests.portal_properties import check_portal_properties
from mars.policy.tests.portal_mailhost   import check_portal_mailhost
from mars.policy.tests.globals import (
    getTestingOptionsFromIni,
    errprint,
    ZOPETESTCASE,
    format_test_title,
    UNTESTED_WARNING,
)


_options = getTestingOptionsFromIni()
FAILS_ON_UNTESTED_ELEMENT = _options['FAILS_ON_UNTESTED_ELEMENT']
TEST_VERBOSE_MODE =  _options['TEST_VERBOSE_MODE']
TEST_SEQUENCE_TITLE = format_test_title('Checking Portal MailHost')

# utilities and basic variables/options
# if you have plone.reload out there add an helper to use in doctests while programming
# just use preload(module) in pdb :)
# it would be neccessary for you to precise each module to reload, this method is also not recursive.
# eg: (pdb) from foo import bar;preload(bar)
# see utils.py for details

# adapt if any need to your testing utils module.
from mars.policy.tests.globals import *

class TestSetup(TestCase):
    """Check Policy."""

    wkf = getWorkflows()

    def afterSetUp(self):
        """."""
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.types = getToolByName(self.portal, 'portal_types')

    def test_portal_properties(self):
        """Check portal properties setted by profile."""
        check_portal_properties(self.portal)

    # print warning if needed
    if not FAILS_ON_UNTESTED_ELEMENT:
        print UNTESTED_WARNING

    def test_mail_host(self):
        """Check portal mailhost setted by profile"""
        check_portal_mailhost(self.portal)

    def test_skin_installed(self):
        """."""
        skins = getToolByName(self.portal, 'portal_skins')
        layer = skins.getSkinPath(SKIN)
        self.failUnless('mars_skin_custom_images' in layer)
        self.failUnless('mars_skin_custom_templates' in layer)
        self.failUnless('mars_skin_styles' in layer)
        self.assertEquals(SKIN, skins.getDefaultSkin())

    def test_products_dependencies_installed(self):
        """."""
        products = getToolByName(self.portal, 'portal_quickinstaller')
        for product in PRODUCT_DEPENDENCIES:
            self.failUnless(products.isProductInstalled(product))

    def test_workflows_installed(self):
        """Check workflows from profile are installed."""
        if self.wkf['contents']:
            for workflow in self.wkf['contents']:
                self.failUnless(workflow in self.workflow.objectIds())

    def test_workflows_mapped(self):
        """Check workflow mapping."""

        # default workflow
        if self.wkf['default'] :
            self.assertEquals((self.wkf['default'], ),
                                self.workflow.getDefaultChain())

        #others
        for portal_type, chain in self.workflow.listChainOverrides():
            if portal_type in self.wkf['bindings']:
                self.assertEquals((self.wkf['bindings'][portal_type], ), chain)


def test_suite():
    """."""
    setup_site()
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite


import logging
import transaction
from Products.CMFCore.utils import getToolByName

from mars.policy import app_config
from mars.policy.app_config import PRODUCT_DEPENDENCIES, EXTENSION_PROFILES
from mars.policy.tests.globals import (
    getTestingOptionsFromIni,
    errprint,
    ZOPETESTCASE,
    UNTESTED_WARNING,
    format_test_title,
)


_options = getTestingOptionsFromIni()
FAILS_ON_UNTESTED_ELEMENT = _options['FAILS_ON_UNTESTED_ELEMENT']
TEST_VERBOSE_MODE =  _options['TEST_VERBOSE_MODE']
TEST_SEQUENCE_TITLE = format_test_title(' Checking Portal Properties')
 


def setupVarious(context):
    """Miscellanous steps import handle.
    """
    logger = logging.getLogger('mars.policy / setuphandler')

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('mars.policy_various.txt') is None:
        return

    portal = context.getSite()


def setupQi(context):
    """Miscellanous steps import handle.
    """
    logger = logging.getLogger('mars.policy / setuphandler')

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('mars.policy_qi.txt') is None:
        return

    portal = context.getSite() 
    portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')
    portal_setup = getToolByName(portal, 'portal_setup')
    logger = logging.getLogger('mars.policy.Install')

    for product in PRODUCT_DEPENDENCIES:
        logger.info('(RE)Installing %s.' % product)
        if not portal_quickinstaller.isProductInstalled(product):
            portal_quickinstaller.installProduct(product)
            transaction.savepoint()


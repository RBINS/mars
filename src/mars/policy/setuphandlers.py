#-*- coding: utf-8 -*-
"""
MARS Portal setup handlers.
"""
from StringIO import StringIO
import transaction
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from marsapp.categories.storage import CAT_CONTAINER

import logging
from Products.CMFCore.utils import getToolByName

from lxml import etree

def setupVarious(context):
    """
    Import various settings.

    Provisional handler that does initialization that is not yet taken
    care of by other handlers.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('mars_various.txt') is None:
        return
    site = context.getSite()
    site.setLayout('welcome.html')
    existing = site.objectIds()
    wftool = getToolByName(site, 'portal_workflow')
    if 'front-page' in existing:
        fp = site['front-page']
        if wftool.getInfoFor(fp, 'review_state') != 'private':
            wftool.doActionFor(fp, 'retract')
        # Exclude from navigation
        fp.update(excludeFromNav=True)

    return


from mars.policy.app_config import PRODUCT_DEPENDENCIES

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


def publish_all(context):            
    url = getToolByName(context, 'portal_url')
    site = url.getPortalObject()
    catalog = getToolByName(site, 'portal_catalog')
    wftool = getToolByName(site, 'portal_workflow')
    brains = catalog.search({
        'path': {'query': 
                 '/'.join(context.getPhysicalPath())},
        'review_state': 'private',
    })

    for fp in brains:
        wftool.doActionFor(fp.getObject(), 'publish')

def createCategories(context):
    """
    Create needed categories container and contained content.
    """
    # Only run step if a flag file is present
    filenames = context.readDataFile('mars_create_categories.txt')
    if filenames is None:
        return
    filenames = [f 
                 for f in filenames.split('\n') 
                 if f and not f.startswith('#') ]
    site = context.getSite()
    if not CAT_CONTAINER in site.objectIds():
        _createObjectByType('Categories Container', 
                            site,
                            id=CAT_CONTAINER,
                            title='Mars Categories', 
                            excludeFromNav=True)
    container = getattr(site, CAT_CONTAINER)
    publish_all(container)
    for filename in filenames:
        datafile = context.readDataFile('categories/'+filename)
        container.importCatsFromText(datafile, filename)

def remove_pacollection(context):
    if context.readDataFile('mars.r.txt') is None:
        return 
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')
    i = 'plone.app.collection'
    if qi.isProductInstalled(i):
        qi.uninstallProducts([i])

def setupCatalog(context):            
    filename = context.readDataFile('marscatalog.xml')
    if filename is None: return 
    url = getToolByName(context, 'portal_url')
    site = url.getPortalObject()
    catalog = getToolByName(site, 'portal_catalog')
    added_indexes = []
    added_columns = []




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
from mars.policy.app_config import PRODUCT_DEPENDENCIES

from lxml import etree

def setupVarious(context):
    """
    Import various settings.

    Provisional handler that does initialization that is not yet taken
    care of by other handlers.
    """
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile(
        'mars.policy_various.txt') is None:
        return
    site = context.getSite()
    existing = site.objectIds()
    csvt = getToolByName(site, 'portal_csvreplicatatool')
    portal = getToolByName(site, 
                           'portal_url').getPortalObject()
    csvt.setPlainFormat(True)
    # activate all schemata for all objects.
    csvt.fullactivation()
    struct = {
        'administration':{'t':'Administration',
                          'nav':True,
                          'tp':'Folder'},
        'collections':{'t':'Mars',
                       'nav':True,
                       'tp':'Folder'},
        CAT_CONTAINER: {'t':'Mars Categories',
                        'nav':False,
                        'tp':'Categories Container',},
    }
    for b in struct:
        if not b in portal.objectIds():
            obj = _createObjectByType(
                struct[b]['tp'],
                portal, b)
            obj.processForm()
            obj.setExcludeFromNav(not struct[b]['nav'])
            obj.setTitle(struct[b]['t'])
            publish_all(obj)

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
    filenames = context.readDataFile('mars_categories_container.txt')
    if filenames is None:
        return
    #filenames = [f
    #             for f in filenames.split('\n')
    #             if f and not f.startswith('#') ]
    site = context.getSite()
    if not CAT_CONTAINER in site.objectIds():
        _createObjectByType('Categories Container',
                            site,
                            id=CAT_CONTAINER,
                            title='Mars Categories',
                            excludeFromNav=True)
    container = getattr(site, CAT_CONTAINER)
    publish_all(container)
    #for filename in filenames:
    #    datafile = context.readDataFile('categories/'+filename)
    #    container.importCatsFromText(datafile, filename)

def remove_pacollection(context):
    if context.readDataFile('mars.r.txt') is None:
        return
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')
    i = 'plone.app.collection'
    if qi.isProductInstalled(i):
        qi.uninstallProducts([i])

def setupCatalog(context):
    logger = logging.getLogger('mars.policy / setuphandler')
    site = context.getSite()
    xmlstr = context.readDataFile('marscatalog.xml')
    if xmlstr is None: return
    url = getToolByName(site, 'portal_url')
    site = url.getPortalObject()
    catalog = getToolByName(site, 'portal_catalog')
    added_indexes = []
    dom = etree.fromstring(xmlstr)
    class Iextras(object): pass
    for nindex in dom.xpath('//index'):
        added = False
        extras = Iextras()
        infos = dict(nindex.items())
        name = infos.get('name', '')
        itype = infos.get('meta_type', '')
        properties = {}
        indexed_attr = name
        iextras = nindex.xpath('extra')
        iattrs = nindex.xpath('indexed_attr')
        iproperties = nindex.xpath('property')
        if iextras:
            for p in iextras:
                iname = dict(p.items())['name']
                value = dict(p.items())['value']
                setattr(extras, iname, value)
        if iproperties:
            for p in iproperties:
                t = (p.xpath('text()')[0].strip().lower()
                     == 'true')
                iname = dict(p.items())['name']
                if not iname in properties:
                    properties[iname] = t
        if iattrs:
            lindexed_attr = []
            for att in iattrs:
                iname = dict(att.items())['value']
                if not iname in lindexed_attr:
                    lindexed_attr.append(iname)
            if lindexed_attr:
                indexed_attr = ','.join(lindexed_attr)
        if itype == 'ZCTextIndex':
            k = 'doc_attr'
        else:
            k = 'indexed_attr'
        setattr(extras, k,  indexed_attr)
        if name in catalog.Indexes: continue
        if itype in ['KeywordIndex',
                     'FieldIndex',
                     'ZCTextIndex',
                     'DateIndex',
                    ]:
            added = True
        if added:
            catalog.addIndex(name, itype, extra=extras)
            if len(properties.keys()):
                idx = catalog._catalog.getIndex(name)
                for p in properties:
                    idx._updateProperty(p, properties[p])
            if not name in added_indexes:
                added_indexes.append(name)
    for nindex in dom.xpath('//column'):
        name = dict(nindex.items()).get('value', '').strip()
        if not name in catalog._catalog.schema.keys():
            catalog.addColumn(name)
    for c in added_indexes:
        logger.info('Reindex %s' % c)
        catalog.reindexIndex(c, site.REQUEST)


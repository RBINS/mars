"""
MARS Portal setup handlers.
"""
from StringIO import StringIO
import transaction
from five.localsitemanager import make_objectmanager_site
from zope.app.component.interfaces import ISite
from zope.app.component.hooks import setSite
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.component import queryUtility

from zope.event import notify
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.interfaces import IUserPreferredLanguages
from zope.i18n.locales import locales, LoadLocaleError
from zope.interface import implements

from Acquisition import aq_base, aq_get
from Products.StandardCacheManagers.AcceleratedHTTPCacheManager import \
     AcceleratedHTTPCacheManager
from Products.StandardCacheManagers.RAMCacheManager import \
     RAMCacheManager

from Products.CMFCore.interfaces import IPropertiesTool
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IMigrationTool
from Products.CMFPlone.interfaces import INonInstallable \
                                                    as INonProfileInstallable
from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone import migrations as migs
from Products.CMFPlone.events import SiteManagerCreatedEvent
from Products.CMFPlone.Portal import member_indexhtml
from Products.ATContentTypes.lib import constraintypes
from Products.CMFQuickInstallerTool.interfaces import IQuickInstallerTool
from Products.CMFQuickInstallerTool.interfaces import INonInstallable \
                                                    as INonProductInstallable
from plone.i18n.normalizer.interfaces import IURLNormalizer
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY as CONTEXT_PORTLETS
from plone.app.portlets import portlets

from marsapp.categories.storage import CAT_CONTAINER

from Products.CMFBibliographyAT.setuphandlers import install_transform

class HiddenProducts(object):
    implements(INonProductInstallable)

    def getNonInstallableProducts(self):
        return [
            'NuPlone',
            'ATExtensions',
#            'plone.app.blob',
            'FCKeditor',
            'CMFBibliographyAT',
            'MarsPortal',
            'ATBiblioList', 'ATBiblioStyles',
            'ATBiblioTopic', 'AmazonTool', ]

class HiddenProfiles(object):
    implements(INonProfileInstallable)

    def getNonInstallableProfiles(self):
        return [
            u'Products.CMFBibliographyAT:default',
            u'Products.ATBiblioList:default',
            u'Products.ATBiblioStyles:default',
#            u'plone.app.blob:default',
#            u'plone.app.blob:atfile-replacement',
            u'plone.app.iterate:plone.app.iterate',
            u'plone.app.openid:default',
            u'Products.NuPlone:nuplone',
            ]


def importProducts(context):
    """
    Install needed products.
    """
    # Only run step if a flag file is present
    if context.readDataFile('mars_dependencies.txt') is None:
        return
    site = context.getSite()
    qi = getToolByName(site, 'portal_quickinstaller')
    qi.installProduct('ATExtensions', locked=0, forceProfile=True)
    qi.installProduct('CMFBibliographyAT', locked=0, forceProfile=True)
    #qi.installProduct('ATBiblioTopic', locked=0)
    qi.installProduct('FCKeditor', locked=0)
    qi.installProduct('csvreplicata', locked=0)
    qi.installProduct('iw.fss', locked=0, forceProfile=True)
#    qi.installProduct('marsapp.csvreplicata', locked=0)

def createCategories(context):
    """
    Create needed categories container and contained content.
    """
    # Only run step if a flag file is present
    filenames = context.readDataFile('mars_create_categories.txt')
    if filenames is None:
        return
    filenames = [ f for f in filenames.split('\n') if f and not f.startswith('#') ]
    site = context.getSite()
    if not CAT_CONTAINER in site.objectIds():
        _createObjectByType('Categories Container', site,
                            id=CAT_CONTAINER,
                            title='Mars Categories', excludeFromNav=True)
    container = getattr(site, CAT_CONTAINER)
    for filename in filenames:
        datafile = context.readDataFile('categories/'+filename)
        container.importCatsFromText(datafile, filename)

def importBibliographyVarious(context):
    """
    Calls needed installation steps of CMFBibliographyAT
    """
    site = context.getSite()
    logger = context.getLogger('bibliography')
    out = StringIO()
    install_transform(site, out)
    #autoMigrate(site, out)
    logger.info(out.getvalue())
    
    return 'Various settings from CMFBibliographyAT imported.'


def importVarious(context):
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

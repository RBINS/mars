#-*- coding: utf-8 -*-
from zope.interface import implements

from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Archetypes.public import OrderedBaseFolder
from Products.ATContentTypes.interface import IATDocument
from Products.ATContentTypes.atct import ATDocument

from interfaces import IMarsCollectionObject
from interfaces import ISchemataViewletEnabled

from schemata import MarsCollectionObjectSchema
#from mixin import MarsMixin

from Products.CMFCore.utils import getToolByName

class MarsMixin(object):
    def mars_relative_path(self, cctx):
        purl = getToolByName(self, 'portal_url')
        plone = purl.getPortalObject()
        plonep = len('/'.join(plone.getPhysicalPath()))
        return '/'.join(cctx.getPhysicalPath())[plonep:] 

    def getMarsSite(self):
        if self.portal_type == 'Site':
            return self.mars_relative_path(self)
        return '/collections/sites'

    def getMarsCol(self, files=False):
        ctx = self.aq_inner
        oldctx = ctx
        try:
            while (
                (ctx.portal_type not in ['Plone Site', 'Collection'])
                and (self.mars_relative_path(ctx) not in ['/collections', '/collections/collections'])
            ):
                oldctx = ctx
                ctx = ctx.aq_parent
            if (files
                and (ctx.portal_type == 'Collection')
                and ('files' in ctx.objectIds())):
                ctx = ctx['files']
        except Exception, e:
            ctx = oldctx
        return self.mars_relative_path(ctx)

    def getMarsColFiles(self):
        return self.getMarsCol(files=True)  

class MarsCollectionObject(OrderedBaseFolder, ATDocument, MarsMixin):
    """Base class for collection objects"""

    implements(ISchemataViewletEnabled,
               #INonStructuralFolder,
               IMarsCollectionObject)

#    schema = MarsCollectionObjectSchema

    # Make sure we get title-to-id generation when an object is created
    _at_rename_after_creation = True

    # This method, from ISelectableBrowserDefault, is used to check whether
    # the "Choose content item to use as deafult view" option will be
    # presented. This makes sense for folders, but not for RichDocument, so
    # always disallow
    def canSetDefaultPage(self):
        return False

    # enable FTP/WebDAV and friends
    PUT = ATDocument.PUT



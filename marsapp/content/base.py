#-*- coding: utf-8 -*-
from zope.interface import implements

from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Archetypes.public import OrderedBaseFolder
from Products.ATContentTypes.interface import IATDocument
from Products.ATContentTypes.atct import ATDocument

from interfaces import IMarsCollectionObject, IMarsObject
from interfaces import ISchemataViewletEnabled

from schemata import MarsCollectionObjectSchema
#from mixin import MarsMixin

from Products.CMFCore.utils import getToolByName

class MarsMixin(object):
    implements((IMarsObject,))
    def mars_relative_path(self, cctx):
        purl = getToolByName(self, 'portal_url')
        plone = purl.getPortalObject()
        plonep = len('/'.join(plone.getPhysicalPath()))
        return '/'.join(cctx.getPhysicalPath())[plonep:] 


    def getMarsSiteOrCol(self, files=False, curations=False):
        if (self.portal_type == 'Site') and not files:
            return self.mars_relative_path(self)
        ctx = self.aq_inner
        oldctx = ctx
        try:
            while (
                (ctx.portal_type not in ['Plone Site', 'Site', 'Collection',])
                and (
                    self.mars_relative_path(
                        ctx
                    ) not in ['/collections', 
                              '/collections/collections',
                              '/collections/sites']
                )
            ):
                oldctx = ctx
                ctx = ctx.aq_parent
            if (files
                and (ctx.portal_type in ['Site', 'Collection'])
                and ('files' in ctx.objectIds())):
                ctx = ctx['files']
            if (curations
                and (ctx.portal_type in ['Site', 'Collection'])
                and ('curations' in ctx.objectIds())):
                ctx = ctx._getOb('curations')
        except Exception, e:
            ctx = oldctx
        return self.mars_relative_path(ctx) 

    def getMarsSite(self):
        return self.getMarsSiteOrCol()
    def getMarsCol(self, files=False, curations=False):
        return self.getMarsSiteOrCol(files=files, curations=curations)
    def getMarsColFiles(self):
        return self.getMarsCol(files=True)  
    def getMarsColCurations(self):
        return self.getMarsCol(curations=True)   

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



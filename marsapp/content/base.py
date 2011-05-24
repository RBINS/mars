#-*- coding: utf-8 -*-
from zope.interface import implements

from Products.CMFPlone.interfaces import INonStructuralFolder
from Products.Archetypes.public import OrderedBaseFolder
from Products.ATContentTypes.interface import IATDocument
from Products.ATContentTypes.atct import ATDocument

from interfaces import IMarsCollectionObject
from interfaces import ISchemataViewletEnabled

from schemata import MarsCollectionObjectSchema


class MarsCollectionObject(OrderedBaseFolder, ATDocument):
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

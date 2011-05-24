#-*- coding: utf-8 -*-
from zope.component import getUtility

from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
#from Products.CMFCore import permissions

#from Products.Archetypes.Field import Image
from Products.Archetypes.Field import ReferenceField
#from Products.Archetypes.public import DisplayList
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerPropertyType
#from Products.Archetypes.config import TOOL_NAME
#from Products.Archetypes import config

from storage import IMarscatsSettingsStorage
from widget import MarscatWidget

from marsapp.categories.storage import CAT_CONTAINER

def getTitledPath(obj, startup_folder_url, path=None):
    if path is None:
        path = []
    if obj.absolute_url() != startup_folder_url:
        path.insert(0, obj.Title())
        path = getTitledPath(obj.aq_inner.aq_parent, startup_folder_url, path)
    return path

class MarscatField(ReferenceField):
    """ Mars Categories System Field
    """
    _properties = ReferenceField._properties.copy()
    _properties.update({
        'type' : 'marscat',
        'default': None,
        'widget': MarscatWidget,
        'allowed_types': ('Mars Category',),
        'allowed_type_column' : 'portal_type',
        'addable': 1,
        'destination': None,
        'relationship': None,
        'categories': (),
        'index_method' : '_at_edit_accessor',
        })

    security  = ClassSecurityInfo()

    def getStartupDirectory(self, instance):
        storage = getUtility(IMarscatsSettingsStorage)
        portal_type = instance.portal_type
        name = self.getName()
        return storage.getStartupDir(name, portal_type, ispath=True)

    def get(self, instance, **kwargs):
        startup_directory = self.getStartupDirectory(instance)
        portal_url = getToolByName(instance, 'portal_url')
        portal = portal_url.getPortalObject()
        startup_folder = portal.restrictedTraverse(str(startup_directory))
        startup_folder_url = startup_folder.absolute_url()
        refcat = getToolByName(instance, 'reference_catalog')
        items = []
        for uid in ReferenceField.getRaw(self, instance, aslist=True, **kwargs):
            obj = refcat.lookupObject(uid)
            item = getTitledPath(obj, startup_folder_url)
            items.append(' / '.join(item))
        return items


registerField(MarscatField, title='Mars Categories',
              description=('Used for categorizing MARS Collection Objects.'))

registerPropertyType('categories', 'tuple', MarscatField)

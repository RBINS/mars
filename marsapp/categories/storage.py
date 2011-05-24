#-*- coding: utf-8 -*-
from zope.interface import Interface, implements

from persistent import Persistent
from persistent.dict import PersistentDict

CAT_CONTAINER = 'marscategories'

class IMarscatsSettingsStorage(Interface):
    """Utility for defining startup directorie for category fields"""
    
    def setStartupDir():
        """sets startup dir for fieldname"""

    def getStartupDir():
        """returns startup dir for fieldname"""

    def getFieldNames():
        """returns registered marscat field names"""

    def getTypesForField():
        """returns which types have that field"""

class MarscatsSettingsStorage(Persistent):

    implements(IMarscatsSettingsStorage)

    def __init__(self):
        self._fields = PersistentDict()

    def setStartupDir(self, fieldname, startup_dir, portal_type=None):
        field = self._fields.setdefault(fieldname, PersistentDict())
        if portal_type is not None:
            portal_types = field.setdefault('portal_types', PersistentDict())
            portal_types[portal_type] = startup_dir
        else:
            self._fields[fieldname]['startup_directory'] = startup_dir

    def getStartupDir(self, fieldname, portal_type=None,
                            fallback=True, ispath=False):
        sd = ''
        if fallback:
            sd = CAT_CONTAINER
        if fieldname in self._fields.keys():
            field = self._fields.get(fieldname)
            sd = field.get('startup_directory', sd)
            if portal_type is not None:
                pts = field.get('portal_types')
                if pts is not None:
                    sd = pts.get(portal_type, sd)
        if ispath:
            if not sd.startswith(CAT_CONTAINER):
                sd = CAT_CONTAINER + '/' + sd
#            sd = '/' + sd
        return sd

    def getFieldNames(self):
        return list(self._fields)

    def getTypesForField(self, fieldname):
        if fieldname in self._fields:
            field = self._fields[fieldname]
            if 'portal_types' in field and len(field['portal_types']):
                return list(field['portal_types'])
        return list()
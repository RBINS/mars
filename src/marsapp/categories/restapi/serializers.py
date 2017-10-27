# -*- coding: utf-8 -*-
from Products.Archetypes.interfaces import IBaseObject
from Products.Archetypes.interfaces.field import IField
from Products.Archetypes.interfaces.field import IFileField
from Products.Archetypes.interfaces.field import IImageField
from Products.Archetypes.interfaces.field import IReferenceField
from Products.Archetypes.interfaces.field import ITextField
from Products.CMFCore.utils import getToolByName
from plone.app.blob.interfaces import IBlobField
from plone.app.blob.interfaces import IBlobImageField
from plone.restapi.imaging import get_scales
from plone.restapi.interfaces import IFieldSerializer
from plone.restapi.serializer.converters import json_compatible
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer
from plone.restapi.serializer.atfields import DefaultFieldSerializer

from ..interfaces import IMarsCatField

@adapter(IMarsCatField, IBaseObject, Interface)
@implementer(IFieldSerializer)
class MarsCatFieldSerializer(DefaultFieldSerializer):

    def __call__(self):
        accessor = self.field.getAccessor(self.context)
        refs = accessor()
        if refs is None:
            return None
        if self.field.multiValued:
            return json_compatible(refs)
        else:
            return json_compatible(refs)


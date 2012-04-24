#-*- coding: utf-8 -*-

from DateTime import DateTime
from DateTime.interfaces import DateTimeError
from datetime import datetime, date
from Products.Archetypes.Field import ObjectField, Field, DateTimeField
from AccessControl import ClassSecurityInfo
from plone.formwidget.datetime.at import YearWidget
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerPropertyType

class YearField(DateTimeField):
    """A field that stores dates and times"""

    _properties = Field._properties.copy()
    _properties.update({
        'type' : 'datetime',
        'widget' : YearWidget,
        })


registerPropertyType('default', 'datetime', DateTimeField)
registerField(DateTimeField,
              title='Date Time',
              description='Used for storing date/time') 

import os
from cgi import escape

from persistent import Persistent
from persistent.dict import PersistentDict
from persistent.list import PersistentList
from plone.app.form.validators import null_validator
from plone.fieldsets.form import FieldsetsInputForm
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope import schema
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser import ObjectWidget
from zope.app.form.browser import ListSequenceWidget

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from plone.app.controlpanel.interfaces import IPloneControlPanelForm
from plone.app.controlpanel.form import ControlPanelForm

from marsapp.categories.container import MarsCategoriesContainer
from marsapp.categories.storage import IMarscatsSettingsStorage
from marsapp.categories.storage import CAT_CONTAINER


class IPortalTypeMappingField(schema.interfaces.IObject):
    """ """

class PortalTypeMappingField(schema.Object):
    """ """

class IPortalTypesListField(schema.interfaces.IList):
    """ """

class PortalTypesListField(schema.List):
    """ """

class IPortalTypeMapping(Interface):
    portal_type = schema.TextLine(title=u"Portal Type")
    startup_directory = schema.TextLine(title=u"Startup Directory")

class PortalTypeMapping:
    implements(IPortalTypeMapping)
    def __init__(self, portal_type='', startup_directory=''):
        self.portal_type = portal_type
        self.startup_directory = startup_directory


class IFieldMapping(Interface):
    fieldname = schema.TextLine(title=u"Field name (id)")
    startup_directory = schema.TextLine(title=u"Startup Directory")
    portal_types = PortalTypesListField(
        title=u"Portal Types",
        description=u"portal types mapping.",
        required=False,
        default=[],
        value_type=schema.TextLine(title=u"Portal Type"),
        )

class FieldMapping:
    implements(IFieldMapping)
#    def __init__(self, fieldname='', startup_directory=''):
    def __init__(self, fieldname='', startup_directory='', portal_types=[]):
        self.fieldname = fieldname
        self.startup_directory = startup_directory
        self.portal_types = portal_types

class IMarscatSettings(Interface):

    fieldmappings = schema.List(
        title=u"Fields",
        description=u"The Mars Categories Fields.",
        required=True,
        default=[],
        value_type=schema.Object(IFieldMapping, title=u"Field Mapping"),
        )

class MarscatSettings(Persistent):
    implements(IMarscatSettings)
    
    fieldmappings = PersistentList()

class MarscatSettingsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IMarscatSettings)

    def __init__(self, context):
        super(MarscatSettingsControlPanelAdapter, self).__init__(context)
        self.context = getUtility(IMarscatSettings)

    @apply
    def fieldmappings():
        def get(self):
            return [field for field in self.context.fieldmappings]
        def set(self, value):
            stripped = []
            for field in value:
                self.context.fieldmappings = value

        return property(get, set)

fieldmapping_widget = CustomWidgetFactory(ObjectWidget, FieldMapping)
fields_widget = CustomWidgetFactory(ListSequenceWidget,
                                         subwidget=fieldmapping_widget)


class MarscatSettingsControlPanel(ControlPanelForm):
    """A simple form to manage mars categories."""

    form_fields = form.FormFields(IMarscatSettings)
    form_fields['fieldmappings'].custom_widget = fields_widget


    label = _(u'Mars Categories Settings')
    description = _(u"Fields to Mars Categories to fields mappings.")
    form_name = _(u'Categories Settings')



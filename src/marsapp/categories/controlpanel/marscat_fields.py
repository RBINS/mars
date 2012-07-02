#-*- coding: utf-8 -*-
import os
from cgi import escape

from persistent import Persistent
from persistent.dict import PersistentDict
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

class IFieldMapping(Interface):
    startup_directory = schema.TextLine(title=u"tags")
    portal_types = schema.List(
        title=u"Portal Types",
        description=u"portal types mapping.",
        required=True,
        default=[],
        value_type=schema.TextLine(title=u"Toto"),
        )

class FieldMapping:
    implements(IFieldMapping)
    def __init__(self, startup_directory='', portal_types=None):
        self.startup_directory = startup_directory
        self.portal_types = portal_types
        if portal_types == None:
            self.portal_types = []

class IMarscatSettings(Interface):

    fields = schema.List(
        title=u"Fields",
        description=u"The Mars Categories Fields.",
        required=True,
        default=[],
        value_type=schema.TextLine(title=u"Field Mapping"),
        )

class MarscatSettings(Persistent):
    implements(IMarscatSettings)
    
    fields = []


fieldmapping_widget = CustomWidgetFactory(ObjectWidget, FieldMapping)
fields_widget = CustomWidgetFactory(ListSequenceWidget,
                                         subwidget=fieldmapping_widget)

class MarscatSettingsControlPanelAdapter(SchemaAdapterBase):
    adapts(IPloneSiteRoot)
    implements(IMarscatSettings)

    def __init__(self, context):
        super(MarscatSettingsControlPanelAdapter, self).__init__(context)
        self.context = getUtility(IMarscatSettings)

    @apply
    def fields():
        def get(self):
            return [field for field in self.context.fields]
        def set(self, value):
            stripped = []
            for field in value:
                startup_directory = field.startup_directory
                portal_types = field.portal_types
                stripped.append((startup_directory,portal_types))
            self.context.fields = stripped

        return property(get, set)

class MarscatSettingsControlPanel(ControlPanelForm):
    """A simple form to manage mars categories."""

    form_fields = form.FormFields(IMarscatSettings)
    form_fields['fields'].custom_widget = fields_widget

    label = _(u'Mars Categories Settings')
    description = _(u"Fields to Mars Categories to fields mappings.")
    form_name = _(u'Categories Settings')


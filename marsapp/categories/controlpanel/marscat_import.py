#-*- coding: utf-8 -*-
import os
from cgi import escape

from plone.app.form.validators import null_validator
from plone.fieldsets.form import FieldsetsInputForm
from zope.component import adapts
from zope.component import getUtility
from zope.formlib import form
from zope.interface import Interface
from zope.interface import implements
from zope.schema import SourceText

from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from plone.app.controlpanel.interfaces import IPloneControlPanelForm

from marsapp.categories.container import MarsCategoriesContainer
from marsapp.categories.storage import IMarscatsSettingsStorage
from marsapp.categories.storage import CAT_CONTAINER

class IMarscatSchema(Interface):

    cats_import = SourceText(title=_(u'Import Text'),
                           description=_(u"Paste text here."),
                           default=u'',
                           required=False)

class MarscatControlPanel(FieldsetsInputForm):
    """A simple form to manage mars categories."""

    implements(IPloneControlPanelForm, IMarscatSchema)

    template = ZopeTwoPageTemplateFile('marscat_import.pt')
    form_fields = form.FormFields(IMarscatSchema)
    label = _(u'Import Categories')
    description = _(u"From this form, you can import more categories in the system.")
    form_name = _(u'Categories Import')

    def hasCatContainer(self):
        container = getToolByName(self.context, CAT_CONTAINER, None)
        if container is not None:
            return True
        return False

    @form.action(_(u"create_marscats_container",
                   default=u'Create categories repository'),
                 name=u'create_cats')
    def handle_create_catcontainer(self, action, data):
        context = aq_inner(self.context)
        context._setObject(CAT_CONTAINER,
                           MarsCategoriesContainer(CAT_CONTAINER,
                                             title='Mars Categories'))
        context.marscategories.update(excludeFromNav=True)
        self.status = _(u'Created the categories container.')

    @form.action(_(u"import_marscats",
                   default=u'Import'),
                 name=u'import_cats')
    def handle_import_categories(self, action, data):
        context = aq_inner(self.context.marscategories)
        context.importCatsFromText(data['cats_import'])
        self.status = _(u'Imported categories.')


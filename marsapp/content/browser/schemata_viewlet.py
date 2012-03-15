#-*- coding: utf-8 -*-
from zope.component import getMultiAdapter

from plone.app.layout.viewlets.common import ViewletBase

from Acquisition import aq_base, aq_inner, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


INVISIBLE_SCHEMATA = ('metadata', 'dates', 'ownership', 'settings',
                      'attachments')
REMOVED_FROM_SCHEMATA = ('description', 'text')

class SchemataViewlet(ViewletBase):
    render = ViewPageTemplateFile('schemata_viewlet.pt')

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
#        self.portal_url = self.portal_state.portal_url()
        self.membership = getToolByName(self.context, 'portal_membership')


    def getSchemataFields(self, schemata, remove_empty=False):
        context = aq_inner(self.context)
        folder = context.aq_parent
        portal = self.portal_state.portal()
        fields = context.Schema().filterFields(schemata=schemata,
                                               isMetadata=False)
        fields = [ field for field in fields
                   if field.getName() not in REMOVED_FROM_SCHEMATA
                   and self.membership.checkPermission(field.read_permission,
                                                                    context)
                   and field.widget.isVisible(context,'view') == 'visible'
                   and field.widget.testCondition(folder, portal, context)
                   ]
        if remove_empty:
            # we keep only fields that have a value to display
            fields = [ field for field in fields
                       if getattr(context, field.accessor)() ]
        return tuple(fields)

    def getDefaultFields(self, remove_empty=False):
        return self.getSchemataFields('default', remove_empty)

    def getCollapsibleSchemata(self, remove_empty=False):
        schematas = aq_inner(self.context).Schemata()
        fieldsets = [ {'name': key,} for key in schematas.keys()
                      if key not in INVISIBLE_SCHEMATA ]
        for fieldset in fieldsets:
            schemata = fieldset['name']
            fieldset['fields'] = self.getSchemataFields(schemata,
                                                        remove_empty)
        import pdb;pdb.set_trace()  ## Breakpoint ##
        return fieldsets

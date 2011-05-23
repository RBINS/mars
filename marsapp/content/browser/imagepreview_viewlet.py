#from zope.component import getMultiAdapter

from plone.app.layout.viewlets.common import ViewletBase

#from Acquisition import aq_base, aq_inner, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class ImagePreviewViewlet(ViewletBase):
    render = ViewPageTemplateFile('imagepreview_viewlet.pt')

    def update(self):
#        self.portal_state = getMultiAdapter((self.context, self.request),
#                                            name=u'plone_portal_state')
        self.putils = getToolByName(self.context, "plone_utils")
#        self.portal_url = self.portal_state.portal_url()
#        self.membership = getToolByName(self.context, 'portal_membership')


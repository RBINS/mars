#-*- coding: utf-8 -*-
#from Acquisition import aq_base, aq_inner, aq_parent
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName


class welcomePage(BrowserView):
    """MARS Welcome Page
    """
    
    def __init__(self, context, request):
        super(welcomePage, self).__init__(context, request)
        self.membership = getToolByName(context, 'portal_membership')
        self.portal_state = getMultiAdapter((self.context, self.request),
                                                name=u'plone_portal_state')

    __call__ = ZopeTwoPageTemplateFile('templates/welcome-page.pt')


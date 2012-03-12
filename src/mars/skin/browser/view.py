#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Acquisition import aq_parent
from Acquisition import aq_parent


class IMarsUtils(interface.Interface):
    """Marker interface for IMarsUtils"""
    def is_frontpage(context):
        """is frontpage ?"""


class MarsUtils(BrowserView):
    """MarsUtils an image after being edited on a webservice"""
    interface.implements(IMarsUtils)
    def is_frontpage(self, context):
        allowed = ['/mars/front-page',]
        return (
            '/'.join(self.context.getPhysicalPath())
            in allowed
        )
    def is_available(self, context):
        allowed = ['/plone-xcg/front-page',
                   '/plone-xcg/guided-tour',]
        return (
            '/'.join(self.context.getPhysicalPath())
            in allowed
        )

    def __call__(self, *args):
        """."""
        catalog = getToolByName(self.context, 'portal_catalog')
        purl = getToolByName(self.context, 'portal_url')
        plone = purl.getPortalObject()
        import pdb;pdb.set_trace()  ## Breakpoint ##


class IMarsFrontTopicView(interface.Interface):
    """."""

    def __call__(self, *args):
        params = {'test': self.test}
        if self.context.restrictedTraverse('@@xcgutils').is_frontpage(self.context):
            params['front'] = True
        return self.index(**params)

# vim:set et sts=4 ts=4 tw=80:

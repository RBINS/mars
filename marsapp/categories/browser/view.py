# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from archetypes.referencebrowserwidget.interfaces import IReferenceBrowserHelperView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup as b

from Products.Five import BrowserView

from zope.interface import implements, Interface
from plone.app.form._named import named_template_adapter
default_popup_template = named_template_adapter(
    ViewPageTemplateFile('popup.pt'))

class IMarsUtils(Interface):
    """methods"""
    def get_breadcrumbs(context):
        """get_breadcrumbs."""
    def get_parent_breadcrumbs(context):
        """get_parent_breadcrumbs."""

class MarsUtils(BrowserView):
    implements(IMarsUtils)

    def get_breadcrumbs(self, context):
        """get_breadcrumbs."""
        context = aq_inner(context.getObject())
        bc_view = context.restrictedTraverse('@@breadcrumbs_view')
        crumbsd = bc_view.breadcrumbs()
        crumbs = [a['Title'] for a in crumbsd][1:]
        return u' → '.join(crumbs)

    def get_parent_breadcrumbs(self, context):
        """get_proxybreadcrumbs."""
        context = aq_inner(context)
        bc_view = context.restrictedTraverse('@@breadcrumbs_view')
        crumbsd = bc_view.breadcrumbs()
        crumbs = [a['Title'] for a in crumbsd][1:-1]
        crumbs = [a['Title'] for a in crumbsd][1:]
        return u' → '.join(crumbs)

class MarsReferenceBrowserPopup(b, MarsUtils):
    """ A helper view for the reference browser widget."""
    implements((IReferenceBrowserHelperView, IMarsUtils))
    def __init__(self, *args, **kw):
        b.__init__(self, *args, **kw)
        MarsUtils.__init__(self, *args, **kw)

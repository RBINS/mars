# -*- coding: utf-8 -*-   
from Acquisition import aq_inner
from archetypes.referencebrowserwidget.interfaces import \
        IReferenceBrowserHelperView 
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup as b

from zope.interface import implements, Interface
from plone.app.form._named import named_template_adapter
default_popup_template = named_template_adapter(
    ViewPageTemplateFile('popup.pt')) 
class imethods(Interface):
    """methods"""

    def get_breadcrumbs():
        """get_breadcrumbs."""

class MarsReferenceBrowserPopup(b):
    """ A helper view for the reference browser widget."""
    implements((IReferenceBrowserHelperView, imethods))

    def get_breadcrumbs(self, context):
        """get_breadcrumbs."""
        context = aq_inner(context.getObject())
        bc_view = context.restrictedTraverse('@@breadcrumbs_view')
        crumbsd = bc_view.breadcrumbs()
        crumbs = [a['Title'] for a in crumbsd][1:]
        return u' → '.join(crumbs)


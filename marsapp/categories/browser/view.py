# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFPlone.PloneBatch import Batch
from zope.component import getMultiAdapter
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
        return u' → '.join(crumbs)

class MarsReferenceBrowserPopup(b, MarsUtils):
    def getResult(self):
        assert self._updated
        result = []
        qc = getMultiAdapter((self.context, self.request),
                             name='refbrowser_querycatalog')
        if self.widget.show_results_without_query or self.search_text:
            if self.widget.restrict_browsing_to_startup_directory:
                pass
            result = (self.widget.show_results_without_query or \
                      self.search_text) and \
                      qc(search_catalog=self.widget.search_catalog)

            self.has_queryresults = bool(result)

        elif self.widget.allow_browse:
            ploneview = getMultiAdapter((self.context, self.request),
                                        name="plone")
            folder = ploneview.getCurrentFolder()
            self.request.form['path'] = {
                              'query': '/'.join(folder.getPhysicalPath()),
                              'depth':1}
            self.request.form['portal_type'] = []
            result = qc(search_catalog=self.widget.search_catalog)
        else:
            result = []
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))

        return Batch(result, b_size, b_start, orphan=1) 

class MarsCatReferenceBrowserPopup(MarsReferenceBrowserPopup):
    """ A helper view for the reference browser widget."""
    implements((IReferenceBrowserHelperView, IMarsUtils))
    def __init__(self, *args, **kw):
        b.__init__(self, *args, **kw)
        MarsUtils.__init__(self, *args, **kw)

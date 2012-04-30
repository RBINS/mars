# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFPlone.PloneBatch import Batch
from zope.component import getMultiAdapter
from archetypes.referencebrowserwidget.interfaces import IReferenceBrowserHelperView
from archetypes.referencebrowserwidget import utils
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup as b

from Products.Five import BrowserView

from zope.interface import implements, Interface
from plone.app.form._named import named_template_adapter
ref_popup_template = named_template_adapter(
    ViewPageTemplateFile('ref_popup.pt'))
cat_popup_template = named_template_adapter(
    ViewPageTemplateFile('cat_popup.pt'))

class IMarsUtils(Interface):
    """methods"""
    def get_obj_crumb(obj):
        """.""" 
    def get_breadcrumbs(context):
        """get_breadcrumbs."""
    def get_parent_breadcrumbs(context):
        """get_parent_breadcrumbs."""

class MarsUtils(BrowserView):
    implements(IMarsUtils)
    def get_obj_crumb(self, obj, sep='>'):
        """."""
        item = obj.aq_inner
        crumb = []
        while ((item.portal_type not in ['Plone Site'])
               and (item.getId() not in 'marscategories')):
            crumb.append(item.Title() or item.getId())
            item = item.aq_parent
        crumb.reverse()
        return (' %s ' % (sep)).join(crumb) 

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
    implements((IReferenceBrowserHelperView, IMarsUtils))
    def breadcrumbs(self, startup_directory=None):
        assert self._updated
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        bc_view = context.restrictedTraverse('@@breadcrumbs_view')
        crumbs = bc_view.breadcrumbs()

        if not self.widget.restrict_browsing_to_startup_directory:
            newcrumbs = [{'Title': 'Home',
                          'edit_url' : context.absolute_url(),
                          'absolute_url': self.genRefBrowserUrl(
                                portal_state.navigation_root_url())}]
        else:
            # display only crumbs into startup directory
            startup_dir_url = startup_directory or \
                utils.getStartupDirectory(context,
                        self.widget.getStartupDirectory(context, self.field))
            newcrumbs = []
            crumbs = [c for c in crumbs \
                             if c['absolute_url'].startswith(startup_dir_url)]

        for c in crumbs:
            if not 'edit_url' in c:
                c['edit_url'] = '%s' % c['absolute_url']
            c['absolute_url'] = self.genRefBrowserUrl(c['absolute_url'])
            newcrumbs.append(c)

        return newcrumbs 
    def __init__(self, *args, **kw):
        b.__init__(self, *args, **kw)
        MarsUtils.__init__(self, *args, **kw)
    def getResult(self):
        self.request.form['sort_on'] = 'getObjPositionInParent'
        return b.getResult(self)

class MarsCatReferenceBrowserPopup(MarsReferenceBrowserPopup):
    """ A helper view for the reference browser widget."""


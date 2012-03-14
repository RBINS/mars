from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup
from zope.component import getMultiAdapter, queryMultiAdapter
from Acquisition import aq_inner
from archetypes.referencebrowserwidget import utils
from plone.app.form._named import named_template_adapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile 

default_popup_template=named_template_adapter(ViewPageTemplateFile('mars_popup.pt')) 
class MarscatReferenceBrowserPopup(ReferenceBrowserPopup):
    """ View class of Popup window """

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

# vim:set et sts=4 ts=4 tw=80:

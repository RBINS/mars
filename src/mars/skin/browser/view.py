#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from plone.memoize import instance
from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.Archetypes.Widget import RichWidget 
from Acquisition import aq_parent
from Acquisition import aq_parent


from plone.app.content.browser import foldercontents

from Acquisition import aq_inner
from plone.app.content.browser import tableview

import demjson
### ... as well as demjson's
demjson.dumps = demjson.encode
demjson.loads = demjson.decode

from Products.CMFPlone import utils



class Table(tableview.Table):
    """."""
    render = ViewPageTemplateFile("table.pt")
    js = ViewPageTemplateFile("table.js.pt")
    def __init__(self, request, base_url, view_url, items, show_sort_column=False,
                 buttons=[], pagesize=20, show_select_column=True, show_size_column=True,
                 show_modified_column=True, show_status_column=True, id_suf=None): 
        tableview.Table.__init__(self, request, base_url, view_url, items, show_sort_column,
                 buttons, pagesize, show_select_column, show_size_column,
                 show_modified_column, show_status_column)
        self.show_all = True
        self.show_sort_column = False
        self.selection = request.get('select')
        if not id_suf:
            id_suf = '-custom'
        if self.selection == id_suf[1:]:
            self.selectcurrentbatch=True
            self.selectall = True 
        self.id_suf = id_suf

    def get_table_id(self):
        suf = utils.normalizeString(self.id_suf)
        return 'listing-table%s' % suf


    def getJs(self, **jsvars):
        jsvars['tableid'] = self.get_table_id()
        JS = HEADER = ''
        HEADER += "var options = JSON.parse('%s');\n" % demjson.dumps(jsvars)
        js = self.js().replace('%HEADER%', HEADER)
        return js

    @property
    def selectall_url(self):
        return self.selectnone_url+'&select=%s' % self.id_suf[1:]

    @property
    def selectscreen_url(self):
        return self.selectnone_url+'&select=%s' % self.id_suf[1:]

    def selected(self, item):
        ret = False
        if self.selectcurrentbatch:
            ret = True
        return ret


class FolderContentsTable(foldercontents.FolderContentsTable):
    """."""
    def __init__(self, context, request, contentFilter=None, id_suf=None):
        request.set('show_all', 'true')
        foldercontents.FolderContentsTable.__init__(self, context, request, contentFilter)
        url = context.absolute_url()
        view_url = url + '/folder_contents_per_type'
        self.table = Table(request, url, view_url, self.items,
                           show_sort_column=self.show_sort_column,
                           buttons=self.buttons, id_suf=id_suf) 


class IFolderContentsButtons(interface.Interface):
    def button_available():
        """."""

class FolderContentsView(foldercontents.FolderContentsView):
    """."""
    interface.implements(tuple(foldercontents.FolderContentsView.__implemented__)+(
        IFolderContentsButtons,
    ))
    index = ViewPageTemplateFile('folder_contents_per_type.pt')
    def button_available(self):
        object = self.context
        ret = False
        if not isinstance(object, MarsCollectionObject):
            ret = object.displayContentsTab()
        return ret 


    def __init__(self, context, request):
        super(FolderContentsView, self).__init__(context, request)

    def test(self, a, b, c):
        """."""
        return True==bool(a) and b or c 

    @property
    @instance.memoize 
    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(
            {'path':{
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1}
            }
        )
        dres = {}
        for item in brains:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        return dres

    def __call__(self, *args):
        params = {'test': self.test,
                  'myview' : self}

        return self.index(**params) 

    def contents_table(self):
        table = FolderContentsTable(aq_inner(self.context), self.request)
        return table.render()  

    def contents_tables(self):
        tables = {}
        for item  in self.items:
            table = FolderContentsTable(
                aq_inner(self.context), 
                self.request, 
                contentFilter={'portal_type':item},
                id_suf = '-' + item)
            tables[item] = table
        return tables

class IMarsUtils(interface.Interface):
    """Marker interface for IMarsUtils"""
    def is_frontpage(context):
        """is frontpage ?"""
    def related_items(res):
        """related items"""
    def getContentType(object, fieldname):
        """.""" 


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
        #import pdb;pdb.set_trace()  ## Breakpoint ##

    def related_items(self, res):
        """."""
        dres = {}
        for item in res:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        return dres  

    def getContentType(self, object, fieldname):
        """i dont know why but BaseUnit return a
        default text/plain content type for 
        anything else that 'text', just work around 
        to setup well the richwidgets"""
        ct = object.portal_tinymce.getContentType(object=object, fieldname=fieldname)
        field = object.getField(fieldname)
        if isinstance(ct, basestring):
            if 'plain' in ct:
                if isinstance(field.widget, RichWidget):
                    ct = 'text/html'
        return ct


class IMarsFrontTopicView(interface.Interface):
    """."""

class IMarsContentPerType(interface.Interface):
    """."""



from marsapp.content.base import MarsCollectionObject
class MarsContentPerType(BrowserView):
    """."""
    index = ViewPageTemplateFile('folder_contents_per_type.pt')



    def test(self, a, b, c):
        """."""
        return True==bool(a) and b or c

    def group_items(self, res):
        """."""
        dres = {}
        for item in res:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        return dres   

    def __call__(self, *args):
        params = {'test': self.test}
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(
            {'path':{
                'query': '/'.join(self.context.getPhysicalPath()),
                'depth': 1}
            }
        )
        dres = {}
        for item in brains:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        params['data'] = dres   
        return self.index(**params)
 
# vim:set et sts=4 ts=4 tw=80:

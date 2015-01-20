#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from plone.memoize import instance
import logging
from zope import component, interface
from zope.component import getAdapter, getMultiAdapter, queryMultiAdapter, getUtility

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from Products.ATContentTypes.interfaces.interfaces import IATContentType
from Products.Archetypes.Widget import RichWidget
from Acquisition import aq_parent
from marsapp.content.base import MarsCollectionObject
from Acquisition import aq_parent
import transaction

from plone.app.dexterity.browser.types import TypeSchemaContext


from plone.app.content.browser import foldercontents

from marsapp.categories.category import MarsCategory
from marsapp.categories.container import MarsCategoriesContainer
from Acquisition import aq_inner
from plone.app.content.browser import tableview
from marsapp.content.excavation import MarsExcavation

import demjson
### ... as well as demjson's
demjson.dumps = demjson.encode
demjson.loads = demjson.decode

from Products.CMFPlone import utils

from ordereddict import OrderedDict



def get_sorted_dict(d):
    od = OrderedDict()
    ks = d.keys()
    # alpha sort
    ks.sort()
    for k in ks:
        od[k] = d[k]

    # stack wanted types at end
    for otype in ['folder',
                  'Folder']:
        if otype in od:
            del od[otype]
            od[otype] = d[otype]
    return od

def is_bareplone_folderish(item):
    if (   ('Topic' in item.meta_type)
        or ('Folder' in item.meta_type)
        or ('MarsCategor' in item.meta_type)
        or ('Plone Site' == item.meta_type)
       ):
        return True


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


    def folderitems(self):
        items = foldercontents.FolderContentsTable.folderitems(self)
        for item in items:
            if 'view_url' in item:
                if (('folder_contents' in item['view_url'])
                    and (not is_bareplone_folderish(item['brain']))):
                    item['view_url'] = item['view_url'].rsplit(
                        '/folder_contents')[0]
        return items


class FolderContentsView(foldercontents.FolderContentsView):
    """."""
    interface.implements(tuple(foldercontents.FolderContentsView.__implemented__))
    index = ViewPageTemplateFile('folder_contents_per_type.pt')

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)

    def button_available(self):
        """backward compatiblity"""
        return self.context.restrictedTraverse(
            '@@folder_contents_per_type_utils').button_available()


    def test(self, a, b, c):
        """."""
        return True==bool(a) and b or c

    @property
    @instance.memoize
    def items(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.searchResults(
            {
                'path':{
                    'query': '/'.join(self.context.getPhysicalPath()),
                    'depth': 1} ,
                'sort_order': 'getObjPositionInParent'
            }
        )
        dres = {}
        for item in brains:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        return get_sorted_dict(dres)

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
                contentFilter={'portal_type':item, 'sort_order': 'getObjPositionInParent'},
                id_suf = '-' + item)
            tables[item] = table
        return get_sorted_dict(tables)

class IMarsUtils(interface.Interface):
    """Marker interface for IMarsUtils"""
    def is_frontpage(context):
        """is frontpage ?"""
    def related_items(res):
        """related items"""
    def getContentType(object, fieldname):
        """."""
    def infolder_keywords(ctx=None, field='Subject', vocab=None):
        """."""



from mars.skin.utils import infolder_keywords
class MarsUtils(BrowserView):
    """MarsUtils an image after being edited on a webservice"""
    interface.implements(IMarsUtils)

    def infolder_keywords(self, ctx=None, field='Subject'):
        """."""
        if ctx is None:
            ctx = self.context
        return infolder_keywords(ctx, field=field)

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
        try:
            tinymce = object.portal_tinymce
            ctx = object
        except AttributeError:
            # dexteriry
            if isinstance(self.context, TypeSchemaContext):
                tinymce = getToolByName(self.context, 'portal_tinymce')
                ctx = self.context
            else:
                raise
        ct = tinymce.getContentType(object=ctx, fieldname=fieldname)
        field = object.getField(fieldname)
        if isinstance(ct, basestring):
            if 'plain' in ct:
                if isinstance(field.widget, RichWidget):
                    ct = 'text/html'
        return ct



class IFolderContentsButtons(interface.Interface):
    def button_available():
        """."""
    def button_available_for_folder():
        """."""

class FolderContentsViewUtils(BrowserView):
    """."""
    interface.implements(IFolderContentsButtons)
    def button_available(self):
        """."""
        ret, object = False, self.context
        if not isinstance(object, (MarsCollectionObject,
                                   MarsCategory,
                                   MarsCategoriesContainer,
                                   MarsExcavation)):
            ret = object.displayContentsTab()
        return ret
    def button_available_for_folder(self):
        """."""
        ret = False
        if hasattr(self.context, 'meta_type'):
            if is_bareplone_folderish(self.context):
                ret = True
        return ret


class IMarsFrontTopicView(interface.Interface):
    """."""

class IMarsContentPerType(interface.Interface):
    """."""


class MarsContentPerType(BrowserView):
    """."""

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


class IFullReindex(interface.Interface):
        """."""

class FullReindex(BrowserView):
    """."""

    def __call__(self):
        """."""
        logger = logging.getLogger('mars.fullreindex')
        catalog = getToolByName(self.context, 'portal_catalog')
        brains = catalog.search({})
        llen = len(brains)
        for idx, i in enumerate(brains):
            obj = i.getObject()
            try:
                obj.reindexObject()
            except:
                pass
            if idx % 5 == 0:
                transaction.commit()
            if idx % 100 == 0:
                logger.info('%s/%s done' % (idx, llen))
        transaction.commit()



# vim:set et sts=4 ts=4 tw=80:

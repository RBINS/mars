#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
from zope import component, interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_parent, aq_inner

from plone.app.layout.viewlets.common import ViewletBase
import demjson
### ... as well as demjson's
demjson.dumps = demjson.encode
demjson.loads = demjson.decode

from Products.ATContentTypes.interface import IATTopic
from Products.CMFPlone.PloneBatch import Batch
from plone.memoize import ram
from time import time

def five_minutes():
    return time() // (5 * 60)


def fifteen_minutes():
    return time() // (15 * 60)


def _render_details_cachekey(method, self, brain):
    return (brain.getPath()+ fifteen_minutes())


def _render_contents(method, self, *args, **kwargs):
    hs = fifteen_minutes()
    ids = [a for a in self.context.objectIds()]
    ids.sort()
    return (self.context.getPhysicalPath(), ids, hs)


def comparecustom(a):
    """
    sort by author and year."""
    return '%s___%s' % (a.getPath(), a.Title)


class IFacetedDatatableView(interface.Interface):
    """Marker interface"""


class ISummaryView(interface.Interface):
    """Marker interface"""
    def test(a, b, c):
        """."""
    def getContentFilter(contentFilter):
        """."""
    def infosFor(it):
        """."""
    def getFolderContents(contentFilter=None, batch=False,b_size=100,full_objects=False):
        """."""

from mars.skin.utils import ViewMixin
class SummaryView(BrowserView, ViewMixin):
    """MY view doc"""
    interface.implements(ISummaryView)
    #template = ViewPageTemplateFile('template.pt')
    #def __call__(self, **params):
    #    """."""
    #    params = {}
    #    return self.template(**params)

    def test(self, a, b, c):
        if bool(a):
            return b
        else:
            return c


    @ram.cache(_render_contents)
    def getFolderContents(self, contentFilter=None, batch=False,b_size=100,full_objects=False):
        #logging.getLogger('foo').error('cont hitted')
        context = self.context
        mtool = context.portal_membership
        cur_path = '/'.join(context.getPhysicalPath())
        path = {}
        if not contentFilter:
            contentFilter = {}
        else:
            contentFilter = dict(contentFilter)
        if not contentFilter.get('sort_on', None):
            contentFilter['sort_on'] = 'getObjPositionInParent'
        if contentFilter.get('path', None) is None:
            path['query'] = cur_path
            path['depth'] = 1
            contentFilter['path'] = path
        show_inactive = mtool.checkPermission('Access inactive portal content', context)
        # Provide batching hints to the catalog
        b_start = int(context.REQUEST.get('b_start', 0))
        # Evaluate in catalog context because
        # some containers override queryCatalog
        # with their own unrelated method (Topics)
        method = context.portal_catalog.queryCatalog
        if IATTopic.providedBy(self.context):
            method = self.context.queryCatalog
        contents = list(method(
            contentFilter,
            show_all=1,
            show_inactive=show_inactive,))
        if full_objects:
            contents = [b.getObject() for b in contents]
        contents.sort(key=comparecustom)
        if not b_size:
            b_size = len(contents)
        if batch:
            batch = Batch(contents, b_size, b_start, orphan=0)
            return batch
        return contents

    def getContentFilter(self, contentFilter):
        sort_on = self.request.get(
            'sort_on',
            contentFilter.get('sort_on', 'Title'))
        contentFilter['sort_on'] = sort_on
        return contentFilter

    def inmiddle(self, repeat, key):
        """"""
        return (not repeat[key].start and
            not repeat[key].end)

    def last(self, repeat, key):
        """"""
        return repeat[key].end

    def first(self, repeat, key):
        """"""
        return repeat[key].start

    def instrictmiddle(self, repeat, key):
        """"""
        return (self.inmiddle(repeat, key) and
                not self.beforelast(repeat, key))

    def beforelast(self, repeat, key):
        """"""
        ret = False
        rp = repeat[key]
        if self.inmiddle(repeat, key):
            if rp.number() == rp.length()-1:
                ret = True
        return ret

    #@ram.cache(_render_details_cachekey)
    def infosFor(self, it):
        title = it.Title
        path = it.getPath()
        path = path[len(self.root_path):]
        data = {
            'title': title.strip(),
            'path': path,
            'type': it.portal_type,
            'url': it.getURL(),
        }
        return data


class IFacetedDatatablecvMacros(ISummaryView):
    """."""

class FacetedDatatablecvMacros(SummaryView):
    """."""
    def __init__(self, *args, **kwargs):
        SummaryView.__init__(self, *args, **kwargs)

class Search(SummaryView):
    """."""
    def arrange(self, folderContents):
        """ Search using given criteria
        """
        ret = []
        if isinstance(folderContents, Batch):
            # make a list of all batch content
            ret = list(folderContents._sequence)
            ret.sort(key=comparecustom)
        elif folderContents:
            raise Exception(
                'Unexpected folderContents: %s' % type(
                    folderContents))
        return ret


class CSS(ViewletBase):

    def available(self):
        return True

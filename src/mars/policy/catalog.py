#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.indexer import indexer
from plone.dexterity.interfaces import IDexterityItem

from Products.Archetypes.interfaces.base import IBaseContent


def filter_item(obj):
    filtered = False
    if IPloneSiteRoot.providedBy(obj):
        filtered = True
    if obj.getId() == 'organigram':
        filtered = True
    return filtered


def relateditems_fullpathc(obj, titles=None):
    if titles is None:
        titles = list()
    if not hasattr(obj, 'getId') or not hasattr(obj, 'Title'):
        return ()
    if not filter_item(obj):
        titles.insert(0, obj.Title())
        titles = relateditems_fullpathc(obj.aq_inner.aq_parent, titles)
    return tuple(titles)


@indexer(IBaseContent)
def relateditems_fullpath(obj, titles=None):
    items = []
    values = []
    try:
        items = obj.getRelatedItems()
    except Exception:
        pass
    for o in items:
        values.extend(relateditems_fullpathc(o))
    return ' '.join(values)


def _Freedate(item):
    try:
        fd = item.free_date
    except AttributeError:
        try:
            fd = item.Freedate()
        except AttributeError:
            fd = None
    return fd


AFreedate = indexer(IBaseContent)(_Freedate)
BFreedate = indexer(IDexterityItem)(_Freedate)
# vim:set et sts=4 ts=4 tw=80:

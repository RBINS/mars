#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from plone.indexer import indexer
from plone.dexterity.interfaces import IDexterityItem

from Products.Archetypes.interfaces.base import IBaseContent


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

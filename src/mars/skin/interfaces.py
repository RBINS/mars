#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from zope import interface, schema
from plone.theme.interfaces import IDefaultPloneLayer


class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer and a plone skin marker.
    """

class ILayer(interface.Interface):
    """Marker interface that defines a Zope 3 browser layer.
    """ 
 
# vim:set et sts=4 ts=4 tw=80:

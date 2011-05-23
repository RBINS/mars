#!/usr/bin/env python
# encoding: utf-8
"""
content_inspector.py

Created by David Convent on 2008-06-25.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from zope.interface import Interface
#from zope.interface import Attribute
from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot

class IContentInspector(Interface):
    """
    """
    def inspectContent(klass):
        """ Inspect the givent class
        """

class ContentInspector(object):
    """
    """
    implements(IContentInspector)
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        self.context = context
        self.pt = getToolByName(self.context, 'portal_types')

    def inspectContent(self, type_name):
        fti = self.pt.getTypeInfo(type_name)
        result = dict()
        id = 'fakeid'

        if not fti:
            raise ValueError, 'Invalid type %s' % type_name

        result['product'] = fti.product
        # we have to do it all manually :(
#        p = container.manage_addProduct[fti.product]
#        m = getattr(p, fti.factory, None)
#        if m is None:
#            raise ValueError, ('Product factory for %s was invalid' %
#                               fti.getId())
#
#        # construct the object
#        m(id, *args, **kw)
#        ob = container._getOb( id )
#
#        return fti._finishConstruction(ob)
        
        return result

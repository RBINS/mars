# #-*- coding: utf-8 -*-
#
# File: reference.py
#
# Copyright (c) 2008 by ['Eric BREHAULT']
# GNU General Public License (GPL)
#

__author__ = """Eric BREHAULT <eric.brehault@makina-corpus.org>"""
__docformat__ = 'plaintext'

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Field import ReferenceField

from Products.csvreplicata.exceptions import *
from Products.csvreplicata.handlers.base import CSVdefault

import logging
logger = logging.getLogger('HANDLER')
 

from Products.csvreplicata.handlers.reference import CSVReference
        
class CSVMarsCat(CSVReference):
    """
    """
    
    def get(self, obj, field, context=None):
        """
        """
        f = obj.Schema().getField(field)
        value = ReferenceField.getRaw(f, obj, aslist=True)
        #if 'taphono' in f.__name__ and bool(value):
        #    import pdb;pdb.set_trace()  ## Breakpoint ##
        refcat = getToolByName(obj, 'reference_catalog')
        v = []
        startup = f.getStartupDirectory(obj)
        for uid in value:
            target = refcat.lookupObject(uid)
            current = "/".join(obj.getPhysicalPath())+"/"
            path = "/".join(target.getPhysicalPath())
            if path.startswith(current):
                v.append(path[len(current):])
            else:
                v.append(path)
        ret = ''
        if v:
            ret = '\n'.join(v)
        return ret
    
    #def set(self, obj, field, value, context=None):
    #    if value=='':
    #        ref = []
    #    else:
    #        value = value.split('\n')
    #        ref = []
    #        f = obj.Schema().getField(field)
    #        startup = f.getStartupDirectory(obj)
    #        portal_url = getToolByName(obj, 'portal_url')
    #        portal = portal_url.getPortalObject()
    #        for path in value:
    #            try:
    #                complete_path = "/".join(portal.getPhysicalPath())+'/'+startup+path
    #                target = obj.unrestrictedTraverse(complete_path)
    #                ref.append(target)
    #            except Exception:
    #                raise csvreplicataBrokenReferenceException, path+" cannot be found"
    #    self.store(field, obj, ref)
        

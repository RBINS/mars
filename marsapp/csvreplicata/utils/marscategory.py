# -*- coding: utf-8 -*-
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
 
        
class CSVMarsCat(CSVdefault):
    """
    """
    
    def get(self, obj, field, context=None):
        """
        """
        f = obj.Schema().getField(field)
        refcat = getToolByName(obj, 'reference_catalog')
        v = []
        startup = f.getStartupDirectory(obj)
        for uid in ReferenceField.getRaw(f, obj, aslist=True):
            target = refcat.lookupObject(uid)
            url = target.absolute_url()
            path = url[url.index(startup)+len(startup):]
            v.append(path)
        
        return '\n'.join(v)
    
    def set(self, obj, field, value, context=None):
        if value=='':
            ref = []
        else:
            value = value.split('\n')
            ref = []
            f = obj.Schema().getField(field)
            startup = f.getStartupDirectory(obj)
            portal_url = getToolByName(obj, 'portal_url')
            portal = portal_url.getPortalObject()
            for path in value:
                try:
                    complete_path = "/".join(portal.getPhysicalPath())+'/'+startup+path
                    target = obj.unrestrictedTraverse(complete_path)
                    ref.append(target)
                except Exception:
                    raise csvreplicataBrokenReferenceException, path+" cannot be found"
        self.store(field, obj, ref)
        
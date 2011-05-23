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

from Products.csvreplicata.exceptions import *
from Products.csvreplicata.handlers.base import CSVdefault

import logging
logger = logging.getLogger('HANDLER')
 
        
class CSVMarsCoordinates(CSVdefault):
    """
    """
    
    def get(self, obj, field, context=None):
        """
        """
        h = obj.Schema().getField(field).get(obj)
        if h is None:
            return ''
        else:
            l = [str(k)+':'+str(h[k]) for k in h.keys()]
            return "\n".join(l)
    
    def set(self, obj, field, value, context=None):
        if value=='':
            h = None
        else:
            subfields = obj.Schema().getField(field).getSubfields()
            l = value.split('\n')
            h = {}
            for p in l:
                if p!='':
                    try:
                        (k, v) = p.split(':')
                    except Exception, e:
                        raise csvreplicataException, value+" cannot be interpreted as valid coordinates"
                    if k in subfields:
                        h[k] = v
                    else:
                        raise csvreplicataException, k+" is not a valid key in "+field+" (valid keys are:"+",".join(subfields)+")"
            
        self.store(field, obj, str(h))
        
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from datetime import datetime, timedelta
from Products.Archetypes.BaseObject import BaseObject
from Products.Archetypes.Field import ReferenceField
from Products.CMFCore import permissions
import logging
from profilehooks import profile
from ZPublisher.Publish import (
    publish,
    call_object, 
    missing_name, 
    dont_publish_class, 
    mapply) 

from pprint import pprint

timings = {}
def _processForm(self, data=1, metadata=None, REQUEST=None, values=None):
    """patched"""
    ret = getattr(self, '_old__processForm')(
        data=data, 
        metadata=metadata,
        REQUEST=REQUEST, 
        values=values)
    pprint(timings)
    return ret

def _Vocabulary(self, content_instance):
    """patched""" 
    dt1 = datetime.now()
    mykey = '%s_%s' % (
        content_instance.portal_type, 
        self.__name__)
    ret = getattr(self, '_old__Vocabulary')(
        content_instance)
    dt2 = datetime.now()
    dt3 = dt2 - dt1 
    timings[mykey] = dt3 
    return ret

@profile(filename='marsprof')
def profiled_publish(
    request,
    module_name, 
    after_list, 
    debug=0,
    call_object=call_object,
    missing_name=missing_name,
    dont_publish_class=dont_publish_class,
    mapply=mapply): 
    return publish(request, module_name, after_list, 
                   debug, call_object, missing_name, 
                   dont_publish_class, mapply)

def apply_patch(scope, original, replacement):
    log = logger = logging.getLogger('mars.skin.patch')
    try:
        org_dotted_name = '%s.%s.%s' % (scope.__module__, scope.__name__, original)
    except AttributeError, e:
        org_dotted_name = '%s.%s' % (scope.__name__, original)
    new_dotted_name = "%s.%s" % (replacement.__module__, replacement.__name__)
 
    k = '_old_%s'%original
    log.info("Monkey patching %s with %s" % (org_dotted_name, new_dotted_name,))
    setattr(scope, k, getattr(scope, original, None))
    setattr(scope, original, replacement)


# vim:set et sts=4 ts=4 tw=80:

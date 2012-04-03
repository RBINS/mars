#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

import logging

from plone.memoize.instance import memoize
from zope.component import getMultiAdapter, queryMultiAdapter

from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.CMFEditions.Permissions import AccessPreviousVersions
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import log

from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout.viewlets import ViewletBase
from plone.app.layout.viewlets import content

class ContentRelatedItems(content.ContentRelatedItems):

    index = ViewPageTemplateFile("document_relateditems.pt")

    def related_items(self):
        dres = {}
        res = content.ContentRelatedItems.related_items(self)
        for item in res:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        return dres 

# vim:set et sts=4 ts=4 tw=80:

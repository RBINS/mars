#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

import logging

from plone.memoize.instance import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import getToolByName

from plone.app.layout.globals.interfaces import IViewView
from plone.app.layout import viewlets
from plone.app.layout.viewlets import content


class ViewletBaseMixin:
    """."""


class ViewletBase(viewlets.ViewletBase, ViewletBaseMixin):
    """."""

class ContentRelatedItems(content.ContentRelatedItems, 
                          ViewletBaseMixin):

    index = ViewPageTemplateFile("document_relateditems.pt")

    def related_items(self):
        dres = {}
        res = content.ContentRelatedItems.related_items(self)
        for item in res:
            pt = item.portal_type
            if not pt in dres: dres[pt] = []
            dres[pt].append(item)
        return dres 
 

LOGO_ID = 'marslogo.png'
class LogoViewlet(ViewletBase):
    index = ViewPageTemplateFile('logo.pt')
    def update(self):
        super(LogoViewlet, self).update()
        portal = self.portal_state.portal()
        logoTitle = self.portal_state.portal_title()
        self.src = LOGO_ID
        self.navigation_root_title = self.portal_state.navigation_root_title() 



#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
class ViewMixin(object):
    default_language = 'fr'

    @property
    def root(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        return portal_state.navigation_root()

    @property
    def root_path(self):
        return '/'.join(
            self.root.getPhysicalPath()
        )

    @property
    def root_url(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        return portal_state.navigation_root_url()

    @property
    def language(self):
        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )
        return portal_state.language()


    def lang_translate_url(self, context=None, language=None):
        ctx = None
        if context is None:
            ctx = self.context
        elif isinstance(context, basestring):
            if context.startswith('/'):
                ctx = self.context.restrictedTraverse(context)
            else:
                plone = getToolByName(self.context,
                                      'portal_url'
                                     ).getPortalObject()
                ctx = self.context.restrictedTraverse(
                    '/'.join(
                        plone.getPhysicalPath()
                        + (self.antes_default_language,
                           context))
                )
        if language is None:
            language = self.language
        if language != self.default_language:
            brains = ctx.getTranslationBackReferences()
            if brains:
                found = [b for b in brains
                         if b.Language == language]
                if found:
                    ctx = ctx._getReferenceObject(
                        uid=found[0].sourceUID)
        return ctx.absolute_url()

# vim:set et sts=4 ts=4 tw=80:

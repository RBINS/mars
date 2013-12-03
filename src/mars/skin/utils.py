#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
import chardet


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


def magicstring(string):
    """Convert any string to UTF-8 ENCODED one"""
    seek = False
    if isinstance(string, unicode):
        try:
            string = string.encode('utf-8')
        except:
            seek = True
    if seek:
        try:
            detectedenc = chardet.detect(string).get('encoding')
        except Exception, e:
            detectedenc = None
        if detectedenc:
            sdetectedenc = detectedenc.lower()
        else:
            sdetectedenc = ''
        if sdetectedenc.startswith('iso-8859'):
            detectedenc = 'ISO-8859-15'

        found_encodings = [
            'ISO-8859-15', 'TIS-620', 'EUC-KR',
            'EUC-JP', 'SHIFT_JIS', 'GB2312', 'utf-8', 'ascii',
        ]
        if sdetectedenc not in ('utf-8', 'ascii'):
            try:
                if not isinstance(string, unicode):
                    string = string.decode(detectedenc)
                string = string.encode(detectedenc)
            except:
                for idx, i in enumerate(found_encodings):
                    try:
                        if not isinstance(string, unicode) and detectedenc:
                            string = string.decode(detectedenc)
                        string = string.encode(i)
                        break
                    except:
                        if idx == (len(found_encodings) - 1):
                            raise
    if isinstance(string, unicode):
        string = string.encode('utf-8')
    string = string.decode('utf-8').encode('utf-8')
    return string


def infolder_keywords(ctx, field='Subject'):
    """."""
    catalog = getToolByName(ctx, 'portal_catalog')
    purl = getToolByName(ctx, 'portal_url')
    pobj = purl.getPortalObject()
    keywords = []
    ppath = ctx.getPhysicalPath()
    opath = pobj.getPhysicalPath()
    if ppath != opath:
        for k in catalog .searchResults(
            **{
                'path': {
                    'query': '/'.join(ppath[:-1]),
#                    'depth': 0
                }
            }
        ):
            try:
                subjects = getattr(k, field)
                for s in subjects:
                    if not s in keywords:
                        keywords.append(s)
            except:
                continue
    for k in catalog.searchResults(
        **{'path': '/'.join(ppath)}
    ):
        try:
            subjects = getattr(k, field)
            for s in subjects:
                if not s in keywords:
                    keywords.append(s)
        except:
            continue
    allowed_keywords = keywords[:]
    if field in catalog.Indexes.objectIds():
        allowed_keywords = catalog.uniqueValuesFor(field)
    else:
        allowed_keywords = keywords
    allowed_keywords = [a for a in allowed_keywords
                        if a in keywords]
    return keywords

# vim:set et sts=4 ts=4 tw=80:

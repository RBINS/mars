#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'


from zope import interface, component
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory, IContextSourceBinder


from plone.i18n.normalizer.base import baseNormalize

from mars.skin.utils import magicstring, infolder_keywords


def uniquify(t):
    s = []
    [s.append(i) for i in t if not i in s]
    return s


class LocalKeywordFactory(object):
    key = None
    interface.implements(IVocabularyFactory,)

    def __init__(self, key):
        self.key = key

    def __call__(self, context):
        assert self.key is not None
        if isinstance(context, dict):
            context = context.get('context', None)
        values = infolder_keywords(context, self.key)
        values = uniquify(
            [magicstring(a.strip()).decode('utf-8')
             for a in values])
        values.sort()
        values = [
            SimpleTerm(baseNormalize(category).strip(),
                       baseNormalize(category).strip(),
                       category) for category in uniquify(values)]
        return SimpleVocabulary(values)

LocalSubjectsVocabulary = LocalKeywordFactory('Subject')
# vim:set et sts=4 ts=4 tw=80:

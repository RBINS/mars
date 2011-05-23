# -*- coding: utf-8 -*-
###############################################################################
# $Copy$
###############################################################################
""" Export view for the categories

$Id$
"""
__docformat__ = 'reStructuredText'
__author__  = 'David Convent <david.convent@naturalsciences.be>'

# python imports
import logging

# zope2 imports
from Products.CMFCore.utils import getToolByName

# zope3 imports
from zope.interface import Interface
from zope.interface import implements

from storage import CAT_CONTAINER


class IMarscatFlatExporter(Interface):
    """ Interface for MARS Categories export
    """

#    def __call__():
#        """ Execute the renderer """
#
#    def render(resolve_unicode,
#               title_force_uppercase,
#               msdos_eol_style,
#               **kwargs):
#        """ Returns the rendered object(s)
#        object may be a bibliography folder, a single, or a list of
#        bibliography entries
#        """

#log = logging.getLogger('bibliograph.rendering')


class MarscatFlatExporter(object):
    """ A view  """

    implements(IMarscatFlatExporter)

    def __init__(self, context, request):
        self.context = getattr(context, CAT_CONTAINER)
        self.request = request
        self.catalog = getToolByName(self.context, 'portal_catalog')

    def __call__(self):
        return self.createLinesFromCats()

    def createLinesFromCats(self, lines=None, path=None, catseparator=' / '):
        if path is None: path = '/'.join(self.context.getPhysicalPath())
        if lines is None: lines = list()
        brains = self.catalog(portal_type="Mars Category", path={'query': path, 'depth': 1})
        for brain in brains:
            lines.append(catseparator.join(brain.cats_path))
            self.createLinesFromCats(lines, brain.getPath())
        lines.sort(key=str.lower)
        return '\n'.join(lines)

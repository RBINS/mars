#-*- coding: utf-8 -*-
import logging
import re
from StringIO import StringIO
from AccessControl import ClassSecurityInfo
from OFS.ObjectManager import checkValidId

from zope.component import queryUtility

from plone.i18n.normalizer.interfaces import IURLNormalizer

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema

from storage import CAT_CONTAINER

from ordereddict import OrderedDict as odict


log = logging.getLogger('mars.categories.container')

def getEncodedStrings(s):
    if not isinstance(s, basestring):
        raise TypeError
    if isinstance(s, str):
        return s, unicode(s, 'utf-8')
    if isinstance(s, unicode):
        return s.encode('utf-8'), s


_categscache = {}
def getOrCreateCategory(catalog,
                        container, 
                        catname):
    if not isinstance(catname, unicode):
        catname = unicode(catname, 'utf-8')
    catid = queryUtility(IURLNormalizer).normalize(catname)
    catid = catid.replace('"', '').replace("'", '')
    cpath = '%s/%s' % ( container, catid,)
    br = list(
        catalog.search(
            {'path': { 'query': cpath, 'depth' :0}}
        ))
    if not len(br):
        c = _categscache.get(
            container,
            catalog.search(
                {'path': {'query':container, 'depth' :0}}
            )[0].getObject()
        )
        _categscache[container] = c
        _createObjectByType(
            'Mars Category', c, id=catid,
            title=catname, excludeFromNav=True)
        log.info(u'Created category %s' % cpath)
    return cpath

def createCatsFromDict(catalog, containerp, catsdict):
    for catname in catsdict.keys():
        newcatp = getOrCreateCategory(
            catalog, containerp, catname)
        if len(catsdict[catname].keys()) > 0:
            createCatsFromDict(
                catalog, newcatp, catsdict[catname])

schema = ATFolderSchema.copy()

catspat = re.compile(
    r'(/ )|(?:'
    '(?!$)(?: *"((?:.*?"")*'
    '?[^"]*)"|(.*?))'
    '(?: +/ +| +/$| *$))')
twoquotes = re.compile('""')

class MarsCategoriesContainer(ATFolder):
    """A container for Mars Categories"""

    security = ClassSecurityInfo()

    portal_type = archetype_name = "Categories Container"

    schema = schema

    def importCatsFromText(self, text, filename='', catseparator=' / '):
        if '---' not in text:
            if filename is not '':
                print 'Could not import:' + \
                      'no root category defined in %s.' % filename
            else:
                print 'Problem while importing: no root category defined.'
            return
        text.replace('\r\n', '\n')
        lines = text.split('\n')
        lines = [ l.split('#')[0] for l in lines ]
        lines = [ l.strip() for l in lines if l and not l.isspace() ]
        rootname = None
        rootcontainer = None

        catsdict = odict()
        for line in lines:
            if not line.startswith('---'):
                if not catseparator in line \
                and not lines.index(line) == len(lines)-1 \
                and lines[lines.index(line)+1].startswith('---'):
                    rootname = line.strip()
                    catsdict[rootname] = odict()
                else:
                    cats = [ m[2] or twoquotes.sub('"', m[1]) for m in catspat.findall(line) ]
                    if rootname and rootname != cats[0]:
                        cats.insert(0, rootname)
                    parent = catsdict
                    for cat in [ c.strip() for c in cats if c not in ('-',) ]:
                        if cat == '':
                            cat = '(Unnamed category)'
                        if cat not in parent.keys():
                            parent[cat] = dict()
                        parent = parent[cat]
        catalog = getToolByName(self, 'portal_catalog')
        _categscache.clear()
        createCatsFromDict(catalog, 
                           '/'.join(self.getPhysicalPath()), 
                           catsdict)
        log.info('Creation done.')

registerATCT(MarsCategoriesContainer, 'marsapp.categories')

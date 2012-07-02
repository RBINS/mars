#-*- coding: utf-8 -*-
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


def getEncodedStrings(s):
    if not isinstance(s, basestring):
        raise TypeError
    if isinstance(s, str):
        return s, unicode(s, 'utf-8')
    if isinstance(s, unicode):
        return s.encode('utf-8'), s

def getOrCreateCategory(container, catname):
    if not isinstance(catname, unicode):
        catname = unicode(catname, 'utf-8')
    catid = queryUtility(IURLNormalizer).normalize(catname)
    catid = catid.replace('"', '').replace("'", '')
    #print catid
    if catid not in container.objectIds():
        _createObjectByType('Mars Category', container,
                            id=catid,
                            title=catname, excludeFromNav=True)
    return getattr(container, catid)

def createCatsFromDict(container, catsdict):
    for catname in catsdict.keys():
        newcat = getOrCreateCategory(container, catname)
        if len(catsdict[catname].keys()) > 0:
            createCatsFromDict(newcat, catsdict[catname])

schema = ATFolderSchema.copy()

catspat = re.compile(r'(/ )|(?:(?!$)(?: *"((?:.*?"")*?[^"]*)"|(.*?))(?: +/ +| +/$| *$))')
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
        createCatsFromDict(self, catsdict)

registerATCT(MarsCategoriesContainer, 'marsapp.categories')

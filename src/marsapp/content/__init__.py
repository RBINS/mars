# -*- coding: utf-8 -*-
#  mars http://www.naturalsciences.be/metamars/products/
#  Archetypes implementation of the MARS core types based on ATContentTypes
#  Copyright (c) 2003-2007 MARS development team
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""

"""
from Products.Archetypes.Widget import LinesWidget

__docformat__ = 'restructuredtext'

from AccessControl import ModuleSecurityInfo
from zope.i18nmessageid import MessageFactory

from marsapp.categories.category import MarsCategory

from Products.Archetypes import PloneMessageFactory as _
from Products.CMFCore.utils import ContentInit
from Products.ATContentTypes.config import HAS_LINGUA_PLONE

if HAS_LINGUA_PLONE:
    from Products.LinguaPlone.public import process_types
    from Products.LinguaPlone.public import listTypes
else:
    from Products.Archetypes.public import process_types
    from Products.Archetypes.public import listTypes

from config import PROJECTNAME, GLOBALS, I18N_DOMAIN
from permissions import DEFAULT_ADD_CONTENT_PERMISSION
from permissions import ADD_CONTENT_PERMISSIONS

# Import "MarsMessageFactory as _" to create messages in atcontenttypes domain
MarsMessageFactory = MessageFactory(I18N_DOMAIN)
ModuleSecurityInfo(PROJECTNAME).declarePublic('MarsMessageFactory')

import analysis
import artefact
import collection
import curation
import excavation
# import externalfile
import fauna
import flora
import hominid
import institution
# import multimedia
import people
import picture
import site
import stratigraphy
import structure
import pdf

import Products.CMFBibliographyAT.content as CMFBibliographyATContent
from Products.CMFBibliographyAT.content.base import BaseEntry


def initialize(context):
    contentTypes, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types=contentTypes,
        permission=DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)

    for i in range(0, len(contentTypes)):
        klassname = contentTypes[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue
        context.registerClass(
            meta_type=ftis[i]['meta_type'],
            constructors=(constructors[i],),
            permission=ADD_CONTENT_PERMISSIONS[klassname]
        )

    # register custom indexers for relateditems fields
    from zope.component import provideAdapter
    from plone.indexer.decorator import indexer
    from marsapp.content.interfaces import IMarsObject
    from marsapp.content.schemata import vocabularies
    from Products.Archetypes.interfaces.field import IReferenceField
    from Products.CMFCore.utils import getToolByName
    # allow us to index all related fields on title & desc
    for ct in contentTypes:
        for key in ct.schema.keys():
            field = ct.schema[key]
            if (IReferenceField.providedBy(field)
                and not key
                in vocabularies.REFERENCEFIELDS_INDEXES):
                vocabularies.REFERENCEFIELDS_INDEXES[key] = []
                if (not field.accessor
                in vocabularies.REFERENCEFIELDS_INDEXES[
                        key]):
                    vocabularies.REFERENCEFIELDS_INDEXES[
                        key].append(
                        field.accessor
                    )

    def make_reindex_related(index_name):
        iname = index_name

        def reindex_related(obj, *args, **kwargs):
            catalog = getToolByName(obj, 'reference_catalog')
            inamee = iname
            if not inamee in obj.schema.keys():
                return
            field = obj.getField(iname)
            items = field.getRaw(obj)
            indexed = []
            res = ''
            if bool(items):
                if isinstance(items, list):
                    indexed.extend(items)
                else:
                    indexed.append(items)
            for sitem in indexed:
                item = catalog.lookupObject(sitem)
                if isinstance(item, MarsCategory):
                    try:
                        res += ' / '.join(item.cats_path())
                    except:
                        pass
                else:
                    try:
                        res += ' %s' % item.Title()
                    except:
                        pass
                try:
                    res += ' %s' % item.Description()
                except:
                    pass
                try:
                    res += ' %s' % item.description
                except:
                    pass
            if not res:
                res = None
            return res

        return reindex_related

    for field in vocabularies.REFERENCEFIELDS_INDEXES:
        frn = indexer(IMarsObject)(make_reindex_related(field))
        for accessor in vocabularies.REFERENCEFIELDS_INDEXES[field]:
            provideAdapter(frn, name=accessor)


modules = [getattr(CMFBibliographyATContent, c) for c in dir(CMFBibliographyATContent) if not c.startswith('__')]
for module in modules:
    # get all bibliography content classes
    klass = [getattr(module, k) for k in dir(module) if k.endswith('Reference')]
    klass = [k for k in klass if BaseEntry in k.__bases__]
    if klass:
        klass = klass[0]
    else:
        continue

    klass.schema.get('subject').widget.helper_js = ('keywordmultiselect.js',)
    klass.schema.get('keywords').widget = LinesWidget(
        label=_(u'label_keywords', default=u'Keywords'),
        description=_(u'help_keywords',
                      default=u'Categorization of the publications content.'),
        i18n_domain="cmfbibliographyat",
    )

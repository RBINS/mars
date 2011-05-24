#-*- coding: utf-8 -*-
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
__author__  = 'David Convent <david.convent@naturalsciences.be>'
__docformat__ = 'restructuredtext'


from AccessControl import ModuleSecurityInfo
from zope.i18nmessageid import MessageFactory

from Products.CMFCore.DirectoryView import registerDirectory
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
#import externalfile
import fauna
import flora
import hominid
import institution
#import multimedia
import people
import picture
import site
import stratigraphy
import structure
import pdf

def initialize(context):

    contentTypes, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types      = contentTypes,
        permission         = DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    for i in range(0, len(contentTypes)):
        klassname = contentTypes[i].__name__
        if not klassname in ADD_CONTENT_PERMISSIONS:
            continue
        context.registerClass(
            meta_type    = ftis[i]['meta_type'],
            constructors = (constructors[i],),
            permission   = ADD_CONTENT_PERMISSIONS[klassname]
            )
                              

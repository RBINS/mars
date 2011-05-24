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


from api import *
from config import PROJECTNAME
from schemata import *

CollectionSchema = MarsBTreeFolderSchema.copy()
CollectionSchema += CollectionBaseSchema.copy()
CollectionSchema += Schema((

    StringField('source',
        required=False,
        searchable=True,
        vocabulary=collection_source,
        widget=SelectionWidget(label='Source',
            label_msgid='label_collection_source',
            description='Aquisition source of the collection.',
            description_msgid='help_collection_source',
            domain='mars',
            ),
        ),

    ReferenceField('origin',
        searchable=False,
        required=False,
        relationship='belongsTo',
        allowed_types=('Site', 'Excavation'),
        multiValued=True,
        widget=ReferenceBrowserWidget(label='Origin',
            label_msgid='label_collection_origin',
            description='Site or excavation this collection comes from.',
            description_msgid='help_collection_origin',
            domain='mars',
            ),
        ),

    ))
CollectionSchema += AdministrationSchema.copy()
finalizeMarsSchema(CollectionSchema, folderish=True, igNumbers=True)

class MarsCollection(ATBTreeFolder):
    """Collection"""
    schema = CollectionSchema

    portal_type = "Collection"
    archetype_name = "Collection"


registerATCT(MarsCollection, PROJECTNAME)

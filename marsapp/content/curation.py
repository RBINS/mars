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

MarsCurationSchema = MarsBaseSchema.copy() + Schema((
    ReferenceField('curator',  # was 'curat_curator'
        searchable=False,
        required=False,
        allow_browse=True,
        allowed_types=PEOPLE,
        relationship='curatedBy',
        widget=ReferenceBrowserWidget(#add_button?, search functionality,
            label='Curator',
            label_msgid='label_Curator',
            description='Select a curator for this period of time.',
            description_msgid='help_Curator',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        ),

    IntegerField('beginYear',  # was 'curat_begin_date'
        required=False,
        searchable=True,
        size=4,
        widget=IntegerWidget(#forcedigits, lenght=4,
            label='Begin year of curation',
            label_msgid='label_curat_begin_year',
            description='Enter the starting year for this curation.',
            description_msgid='help_curat_begin_year',
            domain='mars',
            starting_year=1830, # not supported by the plone templates yet
            ending_year=None, # not supported by the plone templates yet
            future_years=5, # not supported by the plone templates yet
            ),
        ),

    IntegerField('endYear',  # was 'curat_end_date'
        required=False,
        searchable=True,
        size=4,
        widget=IntegerWidget(#forcedigits, lenght=4,
            label='End date of curation',
            label_msgid='label_curat_end_year',
            description='Enter the ending year for this curation.',
            description_msgid='help_curat_end_year',
            domain='mars',
            starting_year=1830, # not supported by the plone templates yet
            ending_year=None, # not supported by the plone templates yet
            future_years=5, # not supported by the plone templates yet
            ),
        ),

    TextField('history',  # was 'curat_history'
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='History',
            label_msgid='label_history',
            description='Historical review of the major events on the collection item(s) during this curation (moving, exchanges, accidents...).',
            description_msgid='help_curation_history',
            domain='mars',
            ),
        ),
    ))

MarsCurationSchema['title'].widget.label = "Name"
MarsCurationSchema['title'].widget.label_msgid = "label_name"
finalizeATCTSchema(MarsCurationSchema)

class MarsCuration(ATCTContent, MarsMixin):
    """Curation object: represents a small cut in the curation history of a
    collection, a collection object, a reference sample or a multimedia file.
    It has data about 'what' happened when 'who' curated this at 'that' date.
    """
    schema = MarsCurationSchema

    portal_type = "Curation"
    archetype_name = "Curation"


registerATCT(MarsCuration, PROJECTNAME)

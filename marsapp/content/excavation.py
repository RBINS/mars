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

ExcavationSchema = MarsFolderSchema.copy()
ExcavationSchema += Schema((
    StringField('beginningYear',
        #size=4,
        required=True,
        searchable=True,
        #Validator=('isInt','isYear'),
        vocabulary=begin_excavation_years,
        enforce_vocabulary=True,
        widget=SelectionWidget(label='Beginning year',
            label_msgid='label_begin_year',
            description='Enter the beginning year of excavation.',
            description_msgid='help_begin_year',
            domain='mars',
            ),
        ),

    StringField('endingYear',
        #size=4,
        required=False,
        searchable=True,
        #Validator=('isInt','isYear'),
        vocabulary=end_excavation_years,
        enforce_vocabulary=True,
        widget=SelectionWidget(label='Ending year',
            label_msgid='label_end_year',
            description='Enter the year when the excavation ended.',
            description_msgid='help_end_year',
            domain='mars',
            ),
        ),

    TextField('preciseDate',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
       allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Precise Date',
            label_msgid='label_precise_date',
            description='Enter the precise date of excavation, or comments on *when* the excavation was done (YYYY/MM/DD).',
            description_msgid='help_precise_date',
            domain='mars',
            ),
        ),

    ReferenceField('excavators',
        searchable=False,
        required=False,
        multiValued=True,
        relationship='excavatedBy',
        allow_browse=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Excavator(s)',
            label_msgid='label_excavators',
            description='Select the people who made this excavation.',
            description_msgid='help_excavators',
            domain='mars',
            startup_directory='/administration/',
            ),
        schemata='description',
        ),

    TextField('excavationDetails',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Excavation details',
            label_msgid='label_excavators_data',
            description='',
            description_msgid='help_excavation_details',
            domain='mars',
            ),
        schemata='description',
        ),

    ))

ExcavationSchema += InsiteLocationSchema.copy()

ExcavationSchema += Schema((

    ReferenceField('excavationMap',
        searchable=False,
        required=False,
        multiValued=True,
        relationship='inExcavationMap',
        allow_browse=True,
        allowed_types=FILE_AND_FOLDER_TYPES,
        widget=ReferenceBrowserWidget(label='Excavation map(s)',
            label_msgid='label_excavation_map',
            description='Select the map(s) of this excavation.',
            description_msgid='help_excavation_map',
            domain='mars',
            ),
        schemata='description',
        ),

    ))

finalizeMarsSchema(ExcavationSchema)

class MarsExcavation(ATFolder):
    """Excavation"""
    schema = ExcavationSchema

    portal_type = "Excavation"
    archetype_name = "Excavation"


registerATCT(MarsExcavation, PROJECTNAME)

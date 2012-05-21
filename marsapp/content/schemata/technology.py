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


from base import *

TechnologySchema = Schema((

    IntegerField('manufactureYear',
        size=4,
        required=False,
        searchable=False,
        Validator=('isInt','isYear'),
        widget=IntegerWidget(
            label='Year of manufacture',
            label_msgid='label_manufacture_year',
            description='Enter the year of manufacture.',
            description_msgid='help_manufacture_year',
            domain='mars',
            ),
        schemata='technology',
        ),


    #DateTimeField('manufactureYear',
    #    required=False,
    #    searchable=True,
    #    widget=YearWidget(
    #        label='Year of manufacture',
    #        label_msgid='label_manufacture_year',
    #        description='Enter the year of manufacture.', 
    #        description_msgid='help_manufacture_year',
    #        years_range = (-300, 0),
    #        domain='mars',
    #        ),
    #    schemata='technology',
    #    ), 


    TextField('manufacturePreciseDate',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Precise Date',
            label_msgid='label_archeo_manufact_specific',
            description='Enter the precise date of manufacture, or comments on *when* the object was manufactured (YYYY/MM/DD).',
            description_msgid='help_archeo_manufact_specific',
            domain='mars',
            ),
        schemata='technology',
        ),

    ReferenceField('artisan',
        required=False,
        searchable=True,
        relationship="manufacturedBy",
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Artisan',
            label_msgid='label_archeo_ind_name',
            description="Identify the artisan, tribe or culture who made this (e.g. Iliad).",
            description_msgid='help_archeo_ind_name',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata='technology',
        ),

    MarscatField('technologies',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='MadeWith',
        widget=MarscatWidget(label='Technology',
            label_msgid='label_technology',
            description='Technology used',
            description_msgid='help_technology',
            domain='mars',
            startup_directory='/marscategories/technology',
            ),
        schemata='technology',
        ),

    TextField('technologyDetails', 
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Technology details',
            label_msgid='label_relative_cultural_age',
            description='Describe the details on how the techonology was determided',
            description_msgid='help_relative_cultural_age',
            domain='mars',
            ),
        schemata='technology',
        ),

    TextField('functionalDescription',
        searchable=False,
        required=False,
        default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        #default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Functional Description',
            label_msgid='label_functional_description',
            description='What this item was used for.',
            description_msgid='help_functional_description',
            domain='mars',
            ),
        schemata='technology',
        ),

    TextField('usageMarkers',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Markers of Usage',
            label_msgid='label_usage',
            description='Information about usage of the artefact.',
            description_msgid='help_usage',
            domain='mars',
            ),
        schemata='technology',
        ),

    ))

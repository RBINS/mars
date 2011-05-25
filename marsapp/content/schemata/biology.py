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

BiologySchema = Schema((

    MarscatField('taxon',
        required=True,
        searchable=True,
        relationship='hasTaxon',
        widget=MarscatWidget(label='Taxon',
            label_msgid='label_taxon',
            description='Define the taxon as precisely as possible.',
            description_msgid='help_taxon',
            startup_directory='/marscategories/taxa',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('taxonDetermination',
        required=False,
        searchable=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Taxon determination',
            label_msgid='label_taxon_determination',
            description='Features used for taxon determination',
            description_msgid='help_taxon_determination',
            domain='mars',
            ),
        schemata='biology',
        ),

    MarscatField('age',
        required=True,
        searchable=True,
        default='undetermined',
        widget=MarscatWidget(label='Age group',
            label_msgid='label_age',
            description='Select the most appropriate age group.',
            description_msgid='help_age',
            startup_directory='/marscategories/age-group',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('ageDetermination',
        required=False,
        searchable=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Age determination',
            label_msgid='label_age_determination',
            description='Features used for age determination',
            description_msgid='help_age_determination',
            domain='mars',
            ),
        schemata='biology',
        ),

    StringField('gender',
        required=True,
        searchable=False,
        vocabulary=default_gender,
        default='undetermined',
        widget=SelectionWidget(label='Gender',
            label_msgid='label_gender',
            description='Select the gender.',
            description_msgid='help_gender',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('genderDetermination',
        required=False,
        searchable=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Gender determination',
            label_msgid='label_gender_determination',
            description='Features used for gender determination',
            description_msgid='help_gender_determination',
            domain='mars',
            ),
        schemata='biology',
        ),

    MarscatField('pathology',
        required=False,
        searchable=True,
        relationship='sufferedFrom',
        widget=MarscatWidget(label='Pathology',
            label_msgid='label_pathology',
            description='Information about the health status and pathologies.',
            description_msgid='help_pathology',
            startup_directory='/marscategories/pathology',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('pathologyDetermination',
        required=False,
        searchable=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Pathology determination',
            label_msgid='label_pathology_determination',
            description='Features used for pathology determination',
            description_msgid='help_pathology_determination',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('activityMarkers',
        searchable=False,
        required=False,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Markers of activity',
            label_msgid='label_activity',
            description='Information about traces of activity.',
            description_msgid='help_activity',
            domain='mars',
            ),
        schemata='biology',
        ),

    ))

BioIndividualSchema = Schema((

    TextField('causeOfDeath',
        searchable=True,
        required=False,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Cause(s) of death',
            label_msgid='label_cause_of_death',
            description='Information about the cause(s) of death.',
            description_msgid='help_cause_of_death',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('diet',
        searchable=True,
        required=False,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Diet reconstruction',
            label_msgid='label_diet',
            description='Information about diet.',
            description_msgid='help_diet',
            domain='mars',
            ),
        schemata='biology',
        ),

    ))

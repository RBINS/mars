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
__docformat__ = 'restructuredtext'


from base import *

AssemblageSchema = Schema((

    IntegerField('howManyComponents',
        required=False,
        searchable=False,
        widget=IntegerWidget(label='Object Count',
            label_msgid='label_how_many_components',
            description='Overall number of artefacts in the assemblage.',
            description_msgid='help_how_many_components',
            domain='mars',
            ),
        schemata='composition',
        ),

    IntegerField('MNI',
        required=False,
        searchable=False,
        widget=IntegerWidget(label='Minimum number of individuals',
            label_msgid='label_minimum_individuals_ammount',
            description='Minimum number of components present in assemblage.',
            description_msgid='help_minimum_individuals_ammount',
            domain='mars',
            ),
        schemata='composition',
        ),

    TextField('MNIDetermination',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Minimal number of individuals determination',
            label_msgid='label_minimal_ammount_determination',
            description='Features used for determining the minimum number of components.',
            description_msgid='help_minimal_ammount_determination',
            domain='mars',
            ),
        schemata='composition'
        ),

    ReferenceField('components',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='isComposedBy',
        allowed_types=ASSEMBLAGE_COMPONENTS,
        widget=ReferenceBrowserWidget(
            label='Remain components',
            label_msgid='label_remain_components',
            description='Remains composing this assemblage.',
            description_msgid='help_remain_components',
            domain='mars',
            startup_directory_method = 'getMarsCol',
            ),
        schemata='composition',
        ),

    TextField('componentsDistributionDesc',

        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Component distribution',
            label_msgid='label_structure_contents_distribution',
            description="Distribution of the contents inside this assemblage.",
            description_msgid='help_structure_contents_distribution', 
            domain='mars',
            ),
        schemata='composition' 
    ),
    ReferenceField('componentsDistributionFile',
        searchable=False,
        required=False,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        relationship='hasComponentsDistributionFile',
        multiValued=False,
        allowed_types=IMAGE_FILE_AND_FOLDER_TYPES,
        widget=ReferenceBrowserWidget(label='Components Distribution File', # make custom view template showing thumbmail of the map as a link to the map object.
            label_msgid='label_components_distribution_file',
            description='select the Components distribution File',
            description_msgid='help_component_distribution_file',
            domain='mars',
            startup_directory_method='getMarsColFiles',
            ),
        schemata='composition',
        ),


    TextField('attributionInfo',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Attribution Information',
            label_msgid='label_attribution_determination',
            description='Features used for components attribution.',
            description_msgid='help_attribution_determination',
            domain='mars',
            ),
        schemata='composition',
        ),

    ))

BioOriginSchema = Schema((

    StringField('origin',
        required=False,
        searchable=True,
        vocabulary=default_origin,
        multiValued=True,
        default="undetermined",
        widget=SelectionWidget(label='Origin',
            label_msgid='label_origin',
            description='Origin of the assemblage, or what its cause was.',
            description_msgid='help_origin',
            domain='mars',
            ),
        schemata='description',
        ),

    TextField('originDetermination',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Origin Determination',
            label_msgid='label_origin_determination',
            description='Features used for the origin attribution',
            description_msgid='help_origin_determination',
            domain='mars',
            ),
        schemata='description',
        ),

    ))
BioAssemblageSchema = BioOriginSchema + Schema((
    TextField('paleoecology',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Paleoecology',
            label_msgid='label_paleoecology',
            description='Paleological information based on the assemblage',
            description_msgid='help_paleoecology',
            domain='mars',
            ),
        schemata='description'
        ),

    ))

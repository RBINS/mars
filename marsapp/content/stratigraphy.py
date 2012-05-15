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

StratigraphySchema = MarsFolderSchema.copy()
StratigraphySchema += Schema((

    #StringField('substratum',  # was 'strat_substratum'
    #    required=False,
    #    searchable=True,
    #    widget=StringWidget(label='Substratum',
    #        label_msgid='label_substratum',
    #        description="Substratum name?/description?",
    #        description_msgid='help_substratum',
    #        domain='mars',
    #        ),
    #    ),

    MarscatField('substratum',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='composedBy',
        widget=MarscatWidget(label='Substratum',
            label_msgid='label_substratum',
            description="Substratum name?/description?",
            description_msgid='help_substratum',
            domain='mars',
            startup_directory='/marscategories/substratum',
            ),
                 schemata='description',
        ),




    ReferenceField('stratigraphyLayersComposition',
                 schemata='description',
        multiValued=True,
        required=False,
        searchable=True,
        relationship='Composed of strat_layers',
        allowed_types=STRATIGRAPHICAL_LAYER,
        widget=ReferenceBrowserWidget(label='Layers', #add in the view near this Field an overview of the layers composing this stratigraphy.
            label_msgid='label_strat_layers',
            description="Description based on the different assemblages.",
            description_msgid='help_strat_layers',
            domain='mars',
            ),
        ),

    TextField('history',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Historical background',
            label_msgid='label_history',
            description="Older descriptions of the stratigraphy",
            description_msgid='help_stratigraphy_history',
            domain='mars',
            ),
                 schemata='description',
        ),

    ReferenceField('stratigraphyEquivalents',
        allowed_types=('Stratigraphy',),
        multiValued=True,
        searchable=False,
        required=False,
        relationship='equals',
        widget=ReferenceBrowserWidget(label='Equivalent Stratigraphies',
            label_msgid='label_stratigraphy_equivalents',
            description='Stratigraphies from other sites that are the same as this one.',
            description_msgid='help_stratigraphy_equivalents',
            domain='mars',
            startup_directory='/collections/sites/',
            ),
                 schemata='description',
        ),

    ))

StratigraphySchema += ChronologySchema.copy()
StratigraphySchema += ChronologyDatingSchema.copy()
StratigraphySchema += InsiteLocationSchema.copy()
StratigraphySchema += make_coordinates_file_schema()
finalizeMarsSchema(StratigraphySchema, folderish=True, delFields=[])

class MarsStratigraphy(ATFolder, MarsMixin):
    """Stratigraphy"""
    schema = StratigraphySchema

    portal_type = "Stratigraphy"
    archetype_name = "Stratigraphy"


""" Schema for the Stratigraphical Layer.
Non-folderish object (??).
Can be described by a lot of bibliographic references or multimedia instances.
Has been discovered by one or more people.
Belongs to one ore more stratigraphies.
"""
StratigraphicalLayerSchema = MarsFolderSchema.copy()
StratigraphicalLayerSchema += make_coordinates_file_schema()
StratigraphicalLayerSchema += Schema((

    MarscatField('geologicalComponents',
        required=False,
        searchable=True,
        multiValued=True,
        relationship='composedBy',
        widget=MarscatWidget(label='Components',
            label_msgid='label_components',
            description="Associated components composing the stratigraphical assemblage.",
            description_msgid='help_stratigraphy_layer_components',
            startup_directory='/marscategories/geological-components',
            domain='mars',
            ),
        schemata='description',
        ),

    LinesField('featuresDistribution',
        required=False,
        searchable=True,
        widget=LinesWidget(label='Features Distribution',
            label_msgid='label_features_distribution',
            description="Percentile distribution of materials composing the assemblage.",
            description_msgid='help_features_distribution',
            domain='mars',
            ),
        schemata='description',
        ),
    ReferenceField('featuresDistributionFile',
        required=False,
        searchable=False,
        relationship='hasFeaturesDistributionFile',
        allowed_types=FILE_TYPES,
        widget=ReferenceBrowserWidget(label='Features Distribution file',
            label_msgid='label_features_distribution_file',
            description='Upload a file for features distributions.',
            description_msgid='help_features_distribution_file',
            startup_directory_method='getMarsSite',
            domain='mars',
            ),
        schemata='description',
        ),   


    )) + ChronologySchema.copy() + StratigraphyChronologySchema.copy()


finalizeMarsSchema(StratigraphicalLayerSchema, add_synonyms=True)

class MarsStratigraphicalLayer(ATFolder, MarsMixin):
    """Stratigraphical Layer"""
    schema = StratigraphicalLayerSchema

    portal_type = "Stratigraphical Layer"
    archetype_name = "Stratigraphical Layer"


registerATCT(MarsStratigraphy, PROJECTNAME)
registerATCT(MarsStratigraphicalLayer, PROJECTNAME)

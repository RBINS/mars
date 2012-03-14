# #-*- coding: utf-8 -*-   
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

DiscoverySchema = Schema((

    IntegerField('discoveryYear',
        size=4,
        required=False,
        searchable=False,
        Validator=('isInt','isYear'),
        widget=IntegerWidget(label='Discovery year',
            label_msgid='label_discovery_date',
            description='Enter the year of discovery.',
            description_msgid='help_discovery_date',
            domain='mars',
            ),
        schemata='discovery',
        ),

    StringField('datePrecision',
        required=False,
        searchable=True,
        vocabulary=default_date_precision,
        widget=SelectionWidget(label='Date precision',
            label_msgid='label_date_precision',
            description='Select how precise you could give the year.',
            description_msgid='help_date_precision',
            domain='mars',
            ),
        schemata='discovery',
        ),

    TextField('discoveryPreciseDate',
        required=False,
        searchable=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),     
        widget=RichWidget(label='Precise Date',
            label_msgid='label_discovery_precise_date',
            description='Enter the precise date of discovery, or comments on *when* the collection item was discovered (YYYY/MM/DD).',
            description_msgid='help_discovery_precise_date',
            domain='mars',
            ),
        schemata='discovery',
        ),

    ReferenceField('discoverers',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='discoveredBy',
        allow_browse=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Discoverer(s)',
            label_msgid='label_discoverers',
            description='Select the people or institution who found this collection item.',
            description_msgid='help_discoverers',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata='discovery',
        ),

    ReferenceField('stratigraphicalLayer',
        relationship="foundIn",
        allowed_types=STRATIGRAPHICAL_LAYER,
        widget=ReferenceBrowserWidget(label='Stratigraphical Layer',
            label_msgid='label_stratigraphical_layer',
            description='Select the stratigraphical layer in which this item was found.',
            description_msgid='help_stratigraphical_layer',
            domain='mars',
            #startup_directory='/administration/layers',
            ),
        schemata='discovery',
        ),

    ReferenceField('discoverySite',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='extractedFrom',
        allowed_types=('Site',),
        widget=ReferenceBrowserWidget(label='Site',
            label_msgid='label_discovery_site',
            description='Select the site where it was excavated from (as precisely as possible).',
            description_msgid='help_discovery_site',
            domain='mars',
            startup_directory='/collections/sites',
            ),
        schemata='discovery',
        ),

    TextField('discoveryPlace',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),       
        widget=RichWidget(label='Discovery Site',
            label_msgid='label_discovery_place',
            description='Insert information about discovery site if it is not available from the site list.',
            description_msgid='help_discovery_place',
            domain='mars',
            ),
        schemata='discovery',
        ),

    ReferenceField('discoveryExcavation',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='extractedFrom',
        allowed_types=('Excavation',),
        widget=ReferenceBrowserWidget(label='Excavation',
            label_msgid='label_discovery_excavation',
            description='Select the excavation where it was excavated from.',
            description_msgid='help_discovery_excavation',
            domain='mars',
            startup_directory='/collections/sites',
            ),
        schemata='discovery',
        ),

    TextField('discoveryDetails',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Discovery detailed Information',
            label_msgid='label_discovery_details',
            description='Describe the general information about the discovery',
            description_msgid='help_discovery_details',
            domain='mars',
            ),
        schemata='discovery',
        ),

    CoordinatesField('excavationCoordinates', #XXX Only for collection objects
        #XXX Ajouter les champs d'offset.
        #XXX Angle d'offset noté de 0 à 360 dans le sens des aiguilles.
        #XXX éventuellement créer une liste pour caster le choix
        #XXX spécifier également que l'offfset est noté en mètres
        #XXX Les coords dans les carrés doivent aussi être notées en mètres
        required=False,
        searchable=False,
        # Unit, orientation?
        subfields=('XCoordinate',
                   'YCoordinate',
                   'ZCoordinate'),
        # 'Unit'='String', 'Orientation'='String'
        subfield_types={'XCoordinate':'string',
                        'YCoordinate':'string',
                        'ZCoordinate':'string',},
        subfield_labels={'XCoordinate':'X',
                         'YCoordinate':'Y',
                         'ZCoordinate':'Z'},
        Validator='''IsDigital times three?''',
        widget=RecordWidget(label='Numeric excavation coordinates',
            label_msgid='label_excavation_coordinates',
            description='Give the numeric excavation coordinates of where the item was found in its discovery location.',
            description_msgid='help_excavation_coordinates',
            domain='mars',
            ),
        schemata='discovery',
        ),

    ))

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

LocationSchema = Schema((

    StringField('country',
        required=True,
        searchable=False,
        vocabulary=Countries_List,
        widget=SelectionWidget(
            label='Country',
            label_msgid='label_country',
            description='Select the country where the site is located.',
            description_msgid='help_country',
            domain='mars',
            ),
        schemata='location',
        ),

    LinesField('location',
        required=True,
        searchable=False,
        widget=LinesWidget(label='Site Location',
            label_msgid='label_location',
            description="Give an as presise as possible description of the sites location.(e.g.: name of county,name of district,name and distance to closest city,name and distance to closest reference point)",
            description_msgid='help_site_location',
            domain='mars',
            ),
        schemata='location',
        ),

    ReferenceField('map',
        searchable=False,
        required=False,
        relationship='has AdminMap',
        allowed_types=IMAGE_FILE_AND_FOLDER_TYPES,
        startup_directory='library/maps',
        widget=ReferenceBrowserWidget(label='Administrative Map', # make custom view template showing thumbmail of the map as a link to the map object.
            label_msgid='label_administrative_map',
            description='Pick an (administrative) map (as precise as possible) of the region where this site is located.',
            description_msgid='help_site_administrative_map',
            domain='mars',
            startup_directory='/library/maps',
                                     ),
        schemata='location',
        ),

    CoordinatesField('gisCoordinates',
        required=False,
        searchable=False,
        innerJoin=', ',
        outerJoin='<br />',
        subfields=('degrees_EW', 'minutes_EW', 'seconds_EW', 'degrees_NS','minutes_NS', 'seconds_NS', 'altitude', 'unity'), #, 'bool_UpDown'
        subfield_types={'degrees_EW':   'string',
                        'degrees_NS':   'string',
                        'minutes_EW':   'string',
                        'minutes_NS':   'string',
                        'seconds_EW':   'string',
                        'seconds_NS':   'string',
                        'altitude':     'string',
                        #bool_UpDown: 'bool',
                        'unity':        'string',
                        },
        subfield_labels={'degrees_EW':u'Longitude °',
                         'degrees_NS': u'Latitude °',
                         'minutes_EW': "Longitude '",
                         'minutes_NS': "Latitude '",
                         'seconds_EW': 'Longitude "',
                         'seconds_NS': 'Latitude "',
                         'altitude': 'Altitude',
                         #'bool_UpDown':'+/-',
                         'unity':'Unit',
                         },
        #Validator=IsDigital times three?,
        widget=RecordWidget(
            label='GIS coordinates',
            label_msgid='label_GIS_coordinates',
            description='Give the GIS coordinates of the site as precisely in Longitude, Latitude and Altitude',
            description_msgid='help_GIS_coordinates',
            domain='mars',
            ),
        schemata='location',
        ),

    StringField('gisPrecision',
        searchable=False,
        required=True,
        vocabulary=CoordinatesAquisition,
        widget=SelectionWidget(label='GIS Coordinates calculation',
            label_msgid='label_GIS_precision',
            description='Select the way you found the GIS coordinates',
            description_msgid='help_GIS_precision',
            domain='mars',
            ),
        schemata='location',
        ),

    MarscatField('gisProjection',
        searchable=False,
        required=True,
        relationship='hasCoordinatesProjection',
        widget=MarscatWidget(
            label='GIS Coordinates projection',
            label_msgid='label_GIS_projection',
            description='Select the projection system for the GIS coordinates',
            description_msgid='help_GIS_projection',
            startup_directory='/marscategories/coordinate-projection',
            domain='mars',
            ),
        schemata='location',
        ),

    TextField('coordinatesOthers',
        searchable=False,
        required=False,
        #allowable_content_types=('text/plain',),
               default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),       
        widget=RichWidget(label='Other Coordinates',
            label_msgid='label_GIS_others',
            description='Enter the cordinates in other systems like Lambert Coordinates and such',
            description_msgid='help_GIS_others',
            domain='mars',
            ),
        schemata='location',
        ),

    ))

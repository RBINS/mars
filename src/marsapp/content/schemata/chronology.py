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


ChronologySchema = Schema((

    MarscatField('chronologies',
        required=False,
        searchable=False,
        relationship='chronologicalyFits',
        multiValued=True,
        widget=MarscatWidget(label='General Chronologies',
            label_msgid='label_chronology',
            description='Select the fitting chronologies',
            description_msgid='help_chronology',
            startup_directory='/marscategories/chronology',
            domain='mars',
            #show_path=True,
            ),
        schemata='chronology',
        ),

    TextField('chronologyDetails',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
       allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Chronology Details',
            label_msgid='label_chronology_details',
            description='Detailed chronological information.',
            description_msgid='help_chronology_details',
            domain='mars',
            ),
        schemata='chronology',
        ),

        make_dating_analysis(),
    ))

ChronologyDatingSchema = Schema((

    IntegerField('BPDating',
        required=False,
        searchable=False,
        validators=('isInt'),
        widget=IntegerWidget(label='BP Dating',
            label_msgid='label_dating',
            description='"Before Present" dating (Present is 1950).',
            description_msgid='help_dating',
            domain='mars',
            ),
        schemata='chronology',
        ),

    StringField('datingAssociation',
        required=False,
        searchable=False,
        vocabulary=dating_association,
        #Validator=('must if dating not empty'),
        widget=SelectionWidget(label='Dating association',
            label_msgid='label_dating_association',
            description='Select the dating association',
            description_msgid='help_dating_association',
            domain='mars',
            ),
        schemata='chronology',
        ),


    ))

StratigraphyChronologySchema = Schema((
    TextField('relativeGeologicalAge',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Relative Geological age',
            label_msgid='label_relative_geological_age',
            description='Give/Describe the relative geological age.',
            description_msgid='help_relative_geological_age',
            domain='mars',
            ),
        schemata='chronology',
        ),
    ))


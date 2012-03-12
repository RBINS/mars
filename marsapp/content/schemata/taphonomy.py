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

TaphonomySchema = Schema((

    MarscatField('taphonomies',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='alteredBy',
        widget=MarscatWidget(label='Taphonomy(ies)',
            label_msgid='label_geology_taphonomy',
            description='Select all posible activities that this collection item was subjected to.',
            description_msgid='help_geology_taphonomy',
            startup_directory='/marscategories/taphonomy',
            domain='mars',
            ),
        schemata='taphonomy',
        ),

    TextField('taphonomyDetermination',
        required=False,
        searchable=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Taphonomy determination',
            label_msgid='label_geology_taphonomy_determination',
            description='Describe the details on how the taphonomy was determided.',
            description_msgid='help_geology_taphonomy_determination',
            domain='mars',
            ),
        schemata='taphonomy',
        ),

    ))

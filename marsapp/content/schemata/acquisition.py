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

AcquisitionSchema = Schema((

    ReferenceField('author',
        searchable=False,
        required=False,
        multiValued=False,
        relationship='recordedBy',
        allow_browse=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(
            label='Author',
            label_msgid='label_acquis_author',
            description='Person who recorded this sound.',
            description_msgid='help_acquis_author',
            domain='mars',
            ),
        schemata='acquisition',
        ),

    MarscatField('acquisitionProtocole',
        required=False,
        searchable=False,
        multiValued=False,
        relationship='howRecorded',
        widget=MarscatWidget(
            label='Acquisition',
            label_msgid='label_acquis_acquisition',
            description='Select the protocol used to acquire this sound',
            description_msgid='help_acquis_acquisition',
            startup_directory='/marscategories/acquisition-protocol',
            domain='mars',
            ),
        schemata='acquisition',
        ),

    LinesField('AcquisitionComments',
        searchable=True,
        required=False,
        widget=LinesWidget(
            label='Acquisition Comments',
            label_msgid='label_acquis_comment',
            description='Comments from the author.',
            description_msgid='help_acquis_comment',
            domain='mars',
            ),
        schemata='acquisition',
        ),

    ))


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

BurialSchema = Schema((

    StringField('burial',
        required=False,
        searchable=False,
        vocabulary=default_burial,
        widget=SelectionWidget(label='Burial/Sepulcral evidence',
            label_msgid='label_burial',
            description='Was this individual found in a sepulture/burial place?',
            description_msgid='help_burial',
            domain='mars',
            ),
        schemata='description',
        ),

    TextField('burialDetermination',
        required=False,
        searchable=True,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Burial Details',
            label_msgid='label_burial_determination',
            description='Features used for burial determination.',
            description_msgid='help_burial_determination',
            domain='mars',
            ),
        schemata='description',
        ),

    ))


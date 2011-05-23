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

PreservationSchema = Schema((

    StringField('archeologicalStatus',
        required=True,
        searchable=False,
        vocabulary=archeological_status,
        widget=SelectionWidget(label='Status',
            label_msgid='label_archeological_status',
            description='Select the status of the remain.',
            description_msgid='help_archeological_status',
            domain='mars',
            ),
        schemata='description',
        ),

    StringField('preservation',
        required=False,
        searchable=True,
        vocabulary=default_preservation,
        widget=SelectionWidget(label='Preservation',
            label_msgid='label_preservation',
            description='Select from the list.',
            description_msgid='help_choose_from_list',
            domain='mars',
            ),
        schemata='description',
        ),

    ))

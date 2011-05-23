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

MarsPeopleSchema = ATContentTypeSchema.copy() + Schema((
    # identification of the person
    StringField('lastname',  # was 'people_last_name'
        required=True,
        searchable=True,
        widget=StringWidget(label='Last Name',
            label_msgid='label_lastname',
            description="Last Name of this person",
            description_msgid='help_lastname',
            domain='mars',
            ),
        ),

    StringField('prefix',  # was 'people_prefix_name'
        required=False,
        searchable=True,
        widget=StringWidget(label='Prefix of Last Name',
            label_msgid='label_lastname_prefix',
            description="Type the prefix of the name separately (eg: Van, Der, Sir, ...)",
            description_msgid='help_lastname_prefix',
            domain='mars',
            ),
        ),

    StringField('firstname',  # was 'people_first_name'
        required=True,
        searchable=True,
        widget=StringWidget(label='First Name(s)',
            label_msgid='label_firstname',
            description="First name(s) of this person.",
            description_msgid='help_firstname',
            domain='mars',
            ),
        ),

    StringField('peopleStatus',  # was 'people_status'
        required=False,
        searchable=True,
        widget=StringWidget(label='Status or Title',
            label_msgid='label_people_status',
            description="The title or status designing this persons' function/work (eg: Dr in sciences, Chief of Work,...)",
            description_msgid='help_people_status',
            domain='mars',
            ),
        ),

    # contact information
    LinesField('addresses',  # was 'people_address'
        required=False,
        searchable=False,
        default=('street,number,appartment',
                 'zip code/ postal code, City',
                 'Country',
                 'department/section',
                 '...',),
        widget=LinesWidget(label='Address(es)',
            label_msgid='label_addresses',
            description="Enter the address(es) of this person.",
            description_msgid='help_addresses',
            domain='mars',
            ),
        ),

    ReferenceField('institution',   # was 'people_institution'
        searchable=False,
        required=False,
        relationship='worksFor',
        multiValued=True,
        allowed_types=('Institution',),
        widget=ReferenceWidget(label='Institution',
            label_msgid='label_institution',
            description='Pick an institution if this person is working for it.',
            description_msgid='help_institution_reference',
            domain='mars',
            ),
        ),

    LinesField('phones',   # was 'people_phone'
        required=False,
        searchable=False,
        default=('phone:',
                 'GSM:',
                 'other:'),
        # Validator='isPhones',
        widget=LinesWidget(label='Phone number(s)',
            label_msgid='label_phones',
            description="Enter each phone number on a different line (in this format...)",
            description_msgid='help_phones',
            domain='mars',
            ),
        ),

    StringField('url',   # was 'people_url'
        required=False,
        searchable=False,
        # Validator='isURL',
        widget=StringWidget(label='Website',
            label_msgid='label_url',
            description="Give the complete website url.",
            description_msgid='help_url',
            domain='mars',
            ),
        ),

    LinesField('emails',   # was 'people_mail'
        required=False,
        searchable=False,
        # Validator='isEmail',
        widget=LinesWidget(label='Email',
            label_msgid='label_emails',
            description="Give the complete email address(es) of the person.",
            description_msgid='help_emails',
            domain='mars',
            ),
        ),

    # Further information
    TextField('moreInfo',   # was 'people_info'
        searchable=False,
        required=False,
        default_content_type='text/plain',
        allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        widget=TextAreaWidget(label='Further information',
            label_msgid='label_more_info',
            description='General Curriculum Vitae, summarized life story.',
            description_msgid='help_people_more_info',
            domain='mars',
            ),
        ),

    # add in view page template a bibliography Field make a tab listing the publications of this author.
    ))

schema['title'].widget.label = "Name"
schema['title'].widget.label_msgid = "label_name"
MarsPeopleSchema['title'].widget.visible = {
    'edit': 'invisible',
    'view': 'visible',
    }
MarsPeopleSchema['title'].required = 0
finalizeATCTSchema(MarsPeopleSchema)

class MarsPeople(ATCTContent):
    """Any kind of people (archeologist discoverer, authors, site members,
    Analysts, Curators, ... This object only contains the basic information on
    these people, all their personall achievements should be found by doing
    getBrefs() on a people.
    """

    schema = MarsPeopleSchema

    portal_type = "People"
    archetype_name = "People"

    def Title(self):
        name = self.getLastname()
        if self.getPrefix() and self.getPrefix() != '':
            name += ' (' + self.getPrefix() + ')'
        name += ', ' + self.getFirstname()
        return  name


registerATCT(MarsPeople, PROJECTNAME)

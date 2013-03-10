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


from api import *
from config import PROJECTNAME
from schemata import *

INSTITUTION_NATURE = DisplayList((
    ('Make your choice', ''),
    ('Museum','Museum'),
    ('University','University'),
    ('Research institution','Research institution'),
    ('Fundation','Fundation'),
    ('Other','Other'),
    ))

INSTITUTION_STATUS = DisplayList((
    ('Public','Public'),
    ('Private','Private'),
    ))

INSTITUTION_LEVEL = DisplayList((
    ('Make your choice', ''),
    ('International','International'),
    ('National','National'),
    ('Federal','Federal'),
    ('Regional','Regional'),
    ('Other','Other'),
    ))

HeaderSchema = ATContentTypeSchema.copy()
HeaderSchema['title'].widget.label = "Name"
HeaderSchema['title'].widget.label_msgid = "label_name"
HeaderSchema['title'].widget.description = "Institution Name."
HeaderSchema['title'].widget.description_msgid = "help_institution_name"
HeaderSchema['title'].widget.size = "60"

MarsInstitutionSchema = Schema((
    LinesField('synonyms',
        required=False,
        searchable=True,
        widget=LinesWidget(label='Synonyms',
            label_msgid='label_institution_synonym_name',
            description="Alternate Institution Names (one per line).",
            description_msgid='help_institution_synonym_name',
            domain='plone',
            rows=2,
            ),
        ),
    LinesField('address',
        required=False,
#       default=('street, number',
#       'zip code/ postal code, City',
#       'Country',
#       '...',),
        widget=LinesWidget(label='Postal Address',
            label_msgid='label_institution_address',
            domain='plone',
            ),
        ),
    StringField('nature',
        languageIndependent=True,
        required=False,
        vocabulary=INSTITUTION_NATURE,
        widget=SelectionWidget(label='Nature',
            label_msgid='label_institution_nature',
            domain='plone',
            ),
        ),
    StringField('status',
        languageIndependent=True,
        required=False,
        vocabulary=INSTITUTION_STATUS,
        default="Public",
        widget=SelectionWidget(label='Status',
            label_msgid='label_institution_status',
            domain='plone',
            ),
        ),
    StringField('level',
        languageIndependent=True,
        required=False,
        vocabulary=INSTITUTION_LEVEL,
        widget=SelectionWidget(label='Level',
            label_msgid='label_institution_level',
            domain='plone',
            ),
        ),

    LinesField('phone',
        languageIndependent=True,
        required=False,
        default=('phone:',
                 'fax:',
                 'other:'),
        #Validator='isPhones',
        widget=LinesWidget(label='Phone number(s)',
            label_msgid='label_insititution_phone',
            description="One phone number per line respecting the given format.",
            description_msgid='help_insititution_phone',
            domain='plone',
            cols=40,
            rows=3,
            ),
        ),

    StringField('homepage',
        required=False,
        # Validator='isValidHtmlLinkOrEmail',
        widget=StringWidget(label='Homepage',
            label_msgid='label_insititution_homepage',
            #description="One email or url per line.",
            description_msgid='help_insititution_web',
            domain='plone',
            size="60",
            ),
        ),

    LinesField('email',
        languageIndependent=True,
        required=False,
        #Validator='isValidHtmlLinkOrEmail',
        widget=LinesWidget(label='Email Address(es)',
            label_msgid='label_insititution_web',
            description="One email address per line.",
            description_msgid='help_insititution_email',
            domain='plone',
            rows=3,
            cols=80,
            ),
        ),

    TextField('moreInfo',
        searchable=True,
        required=False,
              #default_content_type='text/plain',
              allowable_content_types = ('text/plain',
                                         'text/structured',
                                         'text/html',),
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Presentation',
            label_msgid='label_institution_info',
            description='General presentation and history.',
            description_msgid='help_institution_info',
            domain='plone',
            rows=15,
            ),
        ),
    ))


MarsInstitutionSchema = HeaderSchema + MarsInstitutionSchema
finalizeATCTSchema(MarsInstitutionSchema)

class MarsInstitution(ATCTContent, MarsMixin):
    """Institution
    """

    schema = MarsInstitutionSchema

    portal_type = "Institution"
    archetype_name = "Institution"


registerATCT(MarsInstitution, PROJECTNAME)

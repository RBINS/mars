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
__docformat__ = 'restructuredtext'


from base import *

AdministrationSchema = Schema((

    StringField('insuranceValue',
        read_permission=VIEW_REPOSITORY_PERMISSION,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        searchable=False,
        required=False,
        widget=StringWidget(label='Insurance value',
        label_msgid='label_insurance_value',
            description='The value to be inned by the insurance in case of an accident or theft.',
            description_msgid='help_insurance_value',
            domain='mars',
            ),
        schemata='administration',
        ), 

    ReferenceField('legalProperty',
        searchable=True,
        required=False,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        relationship='ownedBy',
        allow_browse=True,
        multiValued=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Legal property',
            label_msgid='label_legal_property',
            description='Select the person or institute that owns this collection item.',
            description_msgid='help_legal_property',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata='administration',
        ),

    ReferenceField('copyright',
        searchable=True,
        required=False,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        relationship='hasCopyright',
        allow_browse=True,
        multiValued=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Copyright',
            label_msgid='label_legal_copyright',
            description='Select the person or institute that has the copyright on this collection item.',
            description_msgid='help_legal_copyright',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata='administration',
        ),

    ReferenceField('curations',
        searchable=True,
        required=False,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        relationship='curated',
        multiValued=True,
        allowed_types=('Curation',),
        widget=ReferenceBrowserWidget(label='Curation history',
            label_msgid='label_curation_history',
            description='Select the curations this object went through, make new ones if no fitting is found.',
            description_msgid='help_curation_history',
            domain='mars',
            startup_directory_method='getMarsColCurations',
            ),
        schemata='administration',
        ),

    ReferenceField('repository',
        searchable=True,
        required=False,
        multiValued=False,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        relationship='conservatedIn',
        allowed_types=PEOPLE_AND_INSTITUTION,
        startup_directory='administration/organisations',
        widget=ReferenceBrowserWidget(label='Repository',
            label_msgid='label_repository',
            description='Select the institution were this object is in repository now.',
            description_msgid='help_repository',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata='administration',
        ),

    StringField('preciseRepository',
        read_permission=VIEW_REPOSITORY_PERMISSION,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        searchable=True,
        required=False,
        widget=StringWidget(label='Precise repository',
            label_msgid='label_precise_repository',
            description='Give the precise location (as precise as possible) of this object.',
            description_msgid='help_precise_repository',
            domain='mars',
            ),
        schemata='administration',
        ),

    ReferenceField('repositoryLink',
        read_permission=VIEW_REPOSITORY_PERMISSION,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        relationship="isStoredIn",
        # allowed_types=('Institution',),
        widget=ReferenceBrowserWidget(label='Link to Repository',
            label_msgid='label_repository_link',
            description='Select the repository in which this object is.',
            description_msgid='help_repository_link',
            startup_directory='/collections/repository',
            domain='mars',
            ),
        schemata='administration',
        ),

    TextField('repositoryStatus',
        read_permission=VIEW_REPOSITORY_PERMISSION,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),     
        widget=RichWidget(label='Repository status',
            label_msgid='label_repository_status',
            description='Status of this object (e.g. study, exposition, ...)',
            description_msgid='help_repository_status',
            domain='mars',
            ),
        schemata='administration',
        ),

    TextField('repositoryConditions',
        read_permission=VIEW_REPOSITORY_PERMISSION,
        write_permission=EDIT_REPOSITORY_PERMISSION,
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),     
        widget=RichWidget(label='Repository conditions',
            label_msgid='label_repository_conditions',
            description='Describe the conditions under wich this object is being held in repository (e.g. light, temperature, humidity, ...).',
            description_msgid='help_repository_conditions',
            domain='mars',
            ),
        schemata='administration',
        ),

    ))

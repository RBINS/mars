#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

 
from base import *
PathologySchema = Schema((

    MarscatField('pathology',
        required=False,
        searchable=True,
        relationship='sufferedFrom',
        widget=MarscatWidget(label='Pathology',
            label_msgid='label_pathology',
            description='Information about the health status and pathologies.',
            description_msgid='help_pathology',
            startup_directory='/marscategories/pathology',
            domain='mars',
            ),
        schemata='biology',
        ),

    TextField('pathologyDetermination',
        required=False,
        searchable=True,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Pathology determination',
            label_msgid='label_pathology_determination',
            description='Features used for pathology determination',
            description_msgid='help_pathology_determination',
            domain='mars',
            ),
        schemata='biology',
        ), 

))


# vim:set et sts=4 ts=4 tw=80:

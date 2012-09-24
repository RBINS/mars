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
from plone.app.blob.content import ATBlob

from AccessControl import ClassSecurityInfo

#from Products.CMFCore import CMFCorePermissions

#from Products.Archetypes.atapi import *
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import ReferenceField

from Products.ATContentTypes.content.file import ATFileSchema
from Products.ATContentTypes.content.file import ATFile
#from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
#from Products.ATContentTypes.content.base import updateActions
#from Products.ATContentTypes.content.base import ATCTFileContent

from marsapp.categories.widget import ReferenceBrowserWidget

#from Products.ATContentTypes.configuration import zconf

from Products.CMFBibliographyAT.config import REFERENCE_TYPES
REFERENCE_TYPES = REFERENCE_TYPES + ('MarsArchive', 'MarsLetter')

PDFFileSchema = ATFileSchema.copy() + Schema((
    #FileField('file',
    #    required = True,
    #    primary = True,
    #    languageIndependent = True,
    #    storage = FileSystemStorage(),
    #    searchable = False,
    #    validators = (('isNonEmptyFile', V_REQUIRED),
    #                  ('checkFileMaxSize', V_REQUIRED),
    #                  #('isPDF', V_REQUIRED), #XXX why doesn't it work?
    #                  ),
    #    widget = FileWidget(
    #        #description = "Select the file to be added by clicking the 'Browse' button.",
    #        #description_msgid = "help_file",
    #        description = "",
    #        label= "PDF File",
    #        label_msgid = "label_pdf_file",
    #        i18n_domain = "plone",
    #        show_content_type = False,
    #        ),
    #    ),
    ReferenceField('bibref',
        relationship = "isBibReference",
        multiValued = False,
        allowed_types = REFERENCE_TYPES,
        searchable = False,
        widget = ReferenceBrowserWidget(label="Bibliography Reference",
            label_msgid="label_bibreference",
            description_msgid="help__bibreference",
            description="Select the corresponding bibliography reference.",
            i18n_domain="plone",
            startup_directory='/litterature/',
            ),
        ),
    ))

finalizeATCTSchema(PDFFileSchema)
PDFFileSchema['file'].label= "Mars PDF File",
PDFFileSchema['file'].label_msgid = "label_pdf_file",

class MarsPDFFile(ATFile):
    security = ClassSecurityInfo()
    #__implements__ = (getattr(ATFile,'__implements__',()),)

    meta_type                  = 'MarsPDFFile'
    portal_type                = 'MarsPDFFile'
    assocMimetypes = ('application/pdf',)
    assocFileExt   = ('pdf', )

    schema = PDFFileSchema


registerType(MarsPDFFile, PROJECTNAME)

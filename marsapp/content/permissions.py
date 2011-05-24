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


from Products.CMFCore.permissions import setDefaultRoles
from config import PROJECTNAME as PN

# Basic permissions
from Products.CMFCore.permissions import View
from Products.CMFCore.permissions import ModifyPortalContent
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.permissions import AccessContentsInformation
from Products.CMFCore.permissions import ListFolderContents

# Add permissions
AddMarsAnalysis                 = "%s: Add Analysis" %PN
AddMarsAnalysisAbsoluteDating   = "%s: Add Absolute Dating Analysis" %PN
AddMarsAnalysisRelativeDating   = "%s: Add Relative Dating Analysis" %PN
AddMarsArtefact                 = "%s: Add Artefact" %PN
AddMarsArtefactIndividual       = "%s: Add Artefact Individual" %PN
AddMarsArtefactAssemblage       = "%s: Add Artefact Assemblage" %PN
AddMarsReferenceSample          = "%s: Add Reference Sample" %PN
AddMarsArtefactReferenceSample  = "%s: Add Artefact Reference Sample" %PN
AddMarsCollection               = "%s: Add Collection" %PN
AddMarsCuration                 = "%s: Add Curation" %PN
AddMarsExcavation               = "%s: Add Excavation" %PN
AddMarsPDFFile                  = "%s: Add PDF File" %PN
AddMarsFaunaRemain              = "%s: Add Fauna Remain" %PN
AddMarsFaunaIndividual          = "%s: Add Fauna Individual" %PN
AddMarsFaunaAssemblage          = "%s: Add Fauna Assemblage" %PN
AddMarsFaunaReferenceSample     = "%s: Add Fauna Reference Sample" %PN
AddMarsFloraRemain              = "%s: Add Flora Remain" %PN
AddMarsFloraIndividual          = "%s: Add Flora Individual" %PN
AddMarsFloraAssemblage          = "%s: Add Flora Assemblage" %PN
AddMarsFloraReferenceSample     = "%s: Add Flora Reference Sample" %PN
AddMarsHominidRemain            = "%s: Add Hominid Remain" %PN
AddMarsHominidIndividual        = "%s: Add Hominid Individual" %PN
AddMarsHominidAssemblage        = "%s: Add Hominid Assemblage" %PN
AddMarsHominidReferenceSample   = "%s: Add Hominid Reference Sample" %PN
AddMarsInstitution              = "%s: Add Institution" %PN
#AddMarsMediaAudioFile           = "%s: Add Media File" %PN
#AddMarsMediaVideoFile           = "%s: Add Video File" %PN
#AddMarsMediaFlashFile           = "%s: Add Flash File" %PN
#AddMarsMediaObj3DFile           = "%s: Add 3D Object File" %PN
AddMarsPeople                   = "%s: Add People" %PN
#AddMarsPicture                  = "%s: Add Picture" %PN
AddMarsStratigraphy             = "%s: Add Stratigraphy" %PN
AddMarsStratigraphicalLayer     = "%s: Add Stratigraphical Layer" %PN
AddMarsStructureAssemblage      = "%s: Add Structure Assemblage" %PN

BASE_PERMISSIONS = ('Manager','Owner',)
setDefaultRoles(AddMarsAnalysis, BASE_PERMISSIONS)
setDefaultRoles(AddMarsAnalysisAbsoluteDating, BASE_PERMISSIONS)
setDefaultRoles(AddMarsAnalysisRelativeDating, BASE_PERMISSIONS)
setDefaultRoles(AddMarsArtefact, BASE_PERMISSIONS)
setDefaultRoles(AddMarsArtefactIndividual, BASE_PERMISSIONS)
setDefaultRoles(AddMarsArtefactAssemblage, BASE_PERMISSIONS)
setDefaultRoles(AddMarsReferenceSample, BASE_PERMISSIONS)
setDefaultRoles(AddMarsArtefactReferenceSample, BASE_PERMISSIONS)
setDefaultRoles(AddMarsCollection, BASE_PERMISSIONS)
setDefaultRoles(AddMarsCuration, BASE_PERMISSIONS)
setDefaultRoles(AddMarsExcavation, BASE_PERMISSIONS)
setDefaultRoles(AddMarsPDFFile, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFaunaRemain, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFaunaIndividual, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFaunaAssemblage, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFaunaReferenceSample, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFloraRemain, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFloraIndividual, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFloraAssemblage, BASE_PERMISSIONS)
setDefaultRoles(AddMarsFloraReferenceSample, BASE_PERMISSIONS)
setDefaultRoles(AddMarsHominidRemain, BASE_PERMISSIONS)
setDefaultRoles(AddMarsHominidIndividual, BASE_PERMISSIONS)
setDefaultRoles(AddMarsHominidAssemblage, BASE_PERMISSIONS)
setDefaultRoles(AddMarsHominidReferenceSample, BASE_PERMISSIONS)
setDefaultRoles(AddMarsInstitution, BASE_PERMISSIONS)
#setDefaultRoles(AddMarsMediaAudioFile, BASE_PERMISSIONS)
#setDefaultRoles(AddMarsMediaVideoFile, BASE_PERMISSIONS)
#setDefaultRoles(AddMarsMediaFlashFile, BASE_PERMISSIONS)
#setDefaultRoles(AddMarsMediaObj3DFile, BASE_PERMISSIONS)
setDefaultRoles(AddMarsPeople, BASE_PERMISSIONS)
#setDefaultRoles(AddMarsPicture, BASE_PERMISSIONS)
setDefaultRoles(AddMarsStratigraphy, BASE_PERMISSIONS)
setDefaultRoles(AddMarsStratigraphicalLayer, BASE_PERMISSIONS)
setDefaultRoles(AddMarsStructureAssemblage, BASE_PERMISSIONS)

DEFAULT_ADD_CONTENT_PERMISSION = AddPortalContent
ADD_CONTENT_PERMISSIONS = {
    'MarsAnalysis'                : AddMarsAnalysis,
    'MarsAnalysisAbsoluteDating'  : AddMarsAnalysisAbsoluteDating,
    'MarsAnalysisRelativeDating'  : AddMarsAnalysisRelativeDating,
    'MarsArtefact'                : AddMarsArtefact,
    'MarsArtefactIndividual'      : AddMarsArtefactIndividual,
    'MarsArtefactAssemblage'      : AddMarsArtefactAssemblage,
    'MarsReferenceSample'         : AddMarsReferenceSample,
    'MarsArtefactReferenceSample' : AddMarsArtefactReferenceSample,
    'MarsCollection'              : AddMarsCollection,
    'MarsCuration'                : AddMarsCuration,
    'MarsExcavation'              : AddMarsExcavation,
    'MarsPDFFile'            : AddMarsPDFFile,
    'MarsFaunaRemain'             : AddMarsFaunaRemain,
    'MarsFaunaIndividual'         : AddMarsFaunaIndividual,
    'MarsFaunaAssemblage'         : AddMarsFaunaAssemblage,
    'MarsFaunaReferenceSample'    : AddMarsFaunaReferenceSample,
    'MarsFloraRemain'             : AddMarsFloraRemain,
    'MarsFloraIndividual'         : AddMarsFloraIndividual,
    'MarsFloraAssemblage'         : AddMarsFloraAssemblage,
    'MarsFloraReferenceSample'    : AddMarsFloraReferenceSample,
    'MarsHominidRemain'           : AddMarsHominidRemain,
    'MarsHominidIndividual'       : AddMarsHominidIndividual,
    'MarsHominidAssemblage'       : AddMarsHominidAssemblage,
    'MarsHominidReferenceSample'  : AddMarsHominidReferenceSample,
    'MarsInstitution'             : AddMarsInstitution,
#    'MarsMediaAudioFile'          : AddMarsMediaAudioFile,
#    'MarsMediaVideoFile'          : AddMarsMediaVideoFile,
#    'MarsMediaFlashFile'          : AddMarsMediaFlashFile,
#    'MarsMediaObj3DFile'          : AddMarsMediaObj3DFile,
    'MarsPeople'                  : AddMarsPeople,
#    'MarsPicture'                 : AddMarsPicture,
    'MarsStratigraphy'            : AddMarsStratigraphy,
    'MarsStratigraphicalLayer'    : AddMarsStratigraphicalLayer,
    'MarsStructureAssemblage'     : AddMarsStructureAssemblage,
    }

EditRepository = "%s: Edit specific repository data" %PN
ViewRepository = "%s: View specific repository data" %PN

setDefaultRoles(EditRepository, ('Manager','Curator','Owner',))
setDefaultRoles(ViewRepository, ('Manager','Curator','Owner',))

# Rename Permissions for use in code
EDIT_REPOSITORY_PERMISSION   = EditRepository
VIEW_REPOSITORY_PERMISSION   = ViewRepository

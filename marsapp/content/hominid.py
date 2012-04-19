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


from api import *
from config import PROJECTNAME
from schemata import *

HominidBiologySchema = BiologySchema.copy()
#HominidBiologySchema['age'].vocabulary = hominid_age
HominidBiologySchema['gender'].vocabulary = hominid_gender

HominidBioRemainSchema = BioRemainSchema.copy()
HominidBioRemainSchema['polarity'].vocabulary = hominid_polarity
HominidBioRemainSchema['laterality'].vocabulary = hominid_laterality

HominidBiologySchema['taxon'].widget.startup_directory = '/marscategories/taxa/fauna/mammalia/primates/hominidae'



HominidBioAssemblageSchema = BioAssemblageSchema.copy()
HominidBioAssemblageSchema['origin'].vocabulary = hominid_origin
HominidBioOriginSchema = BioOriginSchema.copy()
HominidBioOriginSchema['origin'].vocabulary = hominid_origin 

HominidPreservationSchema = PreservationSchema.copy()
HominidPreservationSchema['preservation'].vocabulary = fauna_preservation

HominidBurialSchema = BurialSchema.copy()
HominidBurialSchema['burial'].vocabulary = hominid_burial


HominidRemainSchema = MarsCollectionObjectSchema.copy()
HominidRemainSchema += HominidPreservationSchema.copy() 
HominidRemainSchema += CollectionObjectBaseSchema.copy()
HominidRemainSchema += HominidBioRemainSchema.copy() 
HominidRemainSchema += HominidBiologySchema.copy() 
HominidRemainSchema += BioOriginSchema.copy()
HominidRemainSchema += HominidBurialSchema.copy() 
HominidRemainSchema += ChronologySchema.copy()
HominidRemainSchema += ChronologyDatingSchema.copy()
HominidRemainSchema += TaphonomySchema.copy()
HominidRemainSchema += DiscoverySchema.copy()
HominidRemainSchema += AdministrationSchema.copy()
HominidRemainSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/hominid'
HominidRemainSchema['taxon'].widget.startup_directory = '/marscategories/taxa/fauna/mammalia/primates/hominidae'
finalizeMarsSchema(HominidRemainSchema, delFields=[], remain_types=HOMINIDS_TYPES, is_collection_object=True)

class MarsHominidRemain(MarsCollectionObject):
    """Hominid Remain"""
    schema = HominidRemainSchema

    portal_type = "Hominid Remain"
    archetype_name = "Hominid Remain"


HominidIndividualSchema = MarsCollectionObjectSchema.copy()
HominidIndividualSchema += HominidPreservationSchema.copy() 
HominidIndividualSchema += CollectionObjectBaseSchema.copy()
HominidIndividualSchema += BioIndividualSchema.copy()
HominidIndividualSchema += AssemblageSchema.copy()
HominidIndividualSchema += BioOriginSchema.copy()
HominidIndividualSchema += HominidBiologySchema.copy() 
HominidIndividualSchema += HominidBurialSchema.copy() 
HominidIndividualSchema += ChronologySchema.copy()
HominidIndividualSchema += ChronologyDatingSchema.copy()
HominidIndividualSchema += TaphonomySchema.copy()
HominidIndividualSchema += DiscoverySchema.copy()
HominidIndividualSchema += AdministrationSchema.copy()
HominidIndividualSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/hominid'
HominidIndividualSchema['taxon'].widget.startup_directory = '/marscategories/taxa/fauna/mammalia/primates/hominidae'
finalizeMarsSchema(HominidIndividualSchema, delFields=[], remain_types=HOMINIDS_TYPES, is_collection_object=True)

class MarsHominidIndividual(MarsCollectionObject):
    """Hominid Individual"""
    schema = HominidIndividualSchema

    portal_type = "Hominid Individual"
    archetype_name = "Hominid Individual"


HominidAssemblageSchema = MarsCollectionObjectSchema.copy()
HominidAssemblageSchema += CollectionObjectBaseSchema.copy()
HominidAssemblageSchema += AssemblageSchema.copy()
HominidAssemblageSchema += HominidBioAssemblageSchema.copy() 
HominidAssemblageSchema += HominidBiologySchema.copy() 
HominidAssemblageSchema += HominidBurialSchema.copy() 
HominidAssemblageSchema += BioIndividualSchema.copy()
HominidAssemblageSchema += ChronologySchema.copy()
HominidAssemblageSchema += ChronologyDatingSchema.copy()
HominidAssemblageSchema += TaphonomySchema.copy()
HominidAssemblageSchema += DiscoverySchema.copy()
HominidAssemblageSchema += AdministrationSchema.copy()
HominidAssemblageSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/hominid'
HominidAssemblageSchema['taxon'].widget.startup_directory = '/marscategories/taxa/fauna/mammalia/primates/hominidae'
finalizeMarsSchema(HominidAssemblageSchema, delFields=[], remain_types=HOMINIDS_TYPES, igNumbers=True, is_assemblage=True, is_collection_object=True)

class MarsHominidAssemblage(MarsCollectionObject):
    """Artefact Assemblage"""
    schema = HominidAssemblageSchema

    portal_type = "Hominid Assemblage"
    archetype_name = "Hominid Assemblage"


HominidRefSampleSchema = MarsCollectionObjectSchema.copy()
HominidRefSampleSchema += CollectionObjectBaseSchema.copy()
HominidRefSampleSchema += RefSampleBonesSchema.copy()
HominidRefSampleSchema += ChronologySchema.copy()
HominidRefSampleSchema += AdministrationSchema.copy()
HominidRefSampleSchema += AssemblageSchema.copy()
HominidRefSampleSchema += HominidBiologySchema.copy() 
HominidRefSampleSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/hominid'
finalizeMarsSchema(HominidRefSampleSchema, delFields=[], remain_types=HOMINIDS_TYPES, igNumbers=True, is_collection_object=True)

class MarsHominidReferenceSample(MarsCollectionObject):
    """Hominid Reference Sample"""
    schema = HominidRefSampleSchema

    portal_type = "Hominid Reference Sample"
    archetype_name = "Hominid Reference Sample"


registerType(MarsHominidRemain, PROJECTNAME)
registerType(MarsHominidIndividual, PROJECTNAME)
registerType(MarsHominidAssemblage, PROJECTNAME)
registerType(MarsHominidReferenceSample, PROJECTNAME)

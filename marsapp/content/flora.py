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

FloraBiologySchema = BiologySchema.copy()
#FloraBiologySchema['age'].vocabulary = flora_age
FloraBiologySchema['gender'].vocabulary = flora_gender

FloraBioRemainSchema = BioRemainSchema.copy()
FloraBioRemainSchema['polarity'].vocabulary = flora_polarity
FloraBioRemainSchema['laterality'].vocabulary = flora_laterality

FloraBioAssemblageSchema = BioAssemblageSchema.copy()
FloraBioAssemblageSchema['origin'].vocabulary = flora_origin

FloraPreservationSchema = PreservationSchema.copy()
FloraPreservationSchema['preservation'].vocabulary = fauna_preservation


FloraBurialSchema = BurialSchema.copy()
FloraBurialSchema['burial'].vocabulary = hominid_burial 


FloraRemainSchema = MarsCollectionObjectSchema.copy()
FloraRemainSchema += FloraPreservationSchema.copy() 
FloraRemainSchema += CollectionObjectBaseSchema.copy()
FloraRemainSchema += FloraBioRemainSchema.copy()
FloraRemainSchema += FloraBiologySchema.copy()
FloraRemainSchema += BioAssemblageSchema.copy()
FloraRemainSchema += ChronologySchema.copy()
FloraRemainSchema += ChronologyDatingSchema.copy()
FloraRemainSchema += TaphonomySchema.copy()
FloraRemainSchema += DiscoverySchema.copy()
FloraRemainSchema += AdministrationSchema.copy()
FloraRemainSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/flora'
FloraRemainSchema['taxon'].widget.startup_directory = '/marscategories/taxa/flora'
finalizeMarsSchema(FloraRemainSchema, igNumbers=True,
                   delFields=(#'pathology',
                              #'pathologyDetermination',
                              'laterality', 'polarity',
                              'discoverySite',
                              'activityMarkers'), remain_types=FLORA_TYPES)

class MarsFloraRemain(MarsCollectionObject):
    """Flora Remain"""
    schema = FloraRemainSchema

    portal_type = "Flora Remain"
    archetype_name = "Flora Remain"


FloraIndividualSchema = MarsCollectionObjectSchema.copy()
FloraIndividualSchema += FloraPreservationSchema.copy() 
FloraIndividualSchema += CollectionObjectBaseSchema.copy()
#FloraIndividualSchema += BioIndividualSchema.copy()
FloraIndividualSchema += FloraBiologySchema.copy() 
FloraIndividualSchema += AssemblageSchema.copy()
FloraIndividualSchema += BioAssemblageSchema.copy()
FloraIndividualSchema += ChronologySchema.copy()
FloraIndividualSchema += ChronologyDatingSchema.copy()
FloraIndividualSchema += TaphonomySchema.copy()
FloraIndividualSchema += FloraBurialSchema.copy()
FloraIndividualSchema += DiscoverySchema.copy()
FloraIndividualSchema += AdministrationSchema.copy()
FloraIndividualSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/flora'
FloraIndividualSchema['taxon'].widget.startup_directory = '/marscategories/taxa/flora'
finalizeMarsSchema(FloraIndividualSchema, igNumbers=True,
                   delFields=('pathology',
                              'pathologyDetermination',
                              'laterality', 'polarity',
                              'discoverySite',
                              'activityMarkers',
                              ), remain_types=FLORA_TYPES)

class MarsFloraIndividual(MarsCollectionObject):
    """Flora Individual"""
    schema = FloraIndividualSchema

    portal_type = "Flora Individual"
    archetype_name = "Flora Individual"


FloraAssemblageSchema = MarsCollectionObjectSchema.copy()
FloraAssemblageSchema += CollectionObjectBaseSchema.copy()
FloraAssemblageSchema += AssemblageSchema.copy()
FloraAssemblageSchema += FloraBioAssemblageSchema.copy() 
FloraAssemblageSchema += FloraBiologySchema.copy() 
FloraAssemblageSchema += FloraBurialSchema.copy()
FloraAssemblageSchema += ChronologySchema.copy()
FloraAssemblageSchema += ChronologyDatingSchema.copy()
FloraAssemblageSchema += TaphonomySchema.copy()
FloraAssemblageSchema += DiscoverySchema.copy()
FloraAssemblageSchema += AdministrationSchema.copy()
FloraAssemblageSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/flora'
FloraAssemblageSchema['taxon'].widget.startup_directory = '/marscategories/taxa/flora'
finalizeMarsSchema(FloraAssemblageSchema, igNumbers=True,
                   delFields=(#'pathology',
                              #'pathologyDetermination',
                              'laterality', 'polarity',
                              'discoverySite',
                              'activityMarkers',
                              ), remain_types=FLORA_TYPES)

class MarsFloraAssemblage(MarsCollectionObject):
    """Artefact Assemblage"""
    schema = FloraAssemblageSchema

    portal_type = "Flora Assemblage"
    archetype_name = "Flora Assemblage"


FloraRefSampleSchema = MarsCollectionObjectSchema.copy()
FloraRefSampleSchema += CollectionObjectBaseSchema.copy()
FloraRefSampleSchema += ChronologySchema.copy()
FloraRefSampleSchema += AdministrationSchema.copy()
FloraRefSampleSchema += AssemblageSchema.copy()
FloraRefSampleSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/flora'
#FloraRefSampleSchema['taxon'].widget.startup_directory = '/marscategories/taxa/flora'
finalizeMarsSchema(FloraRefSampleSchema, delFields=[ 'laterality', 'polarity', 'discoverySite'], remain_types=FLORA_TYPES, igNumbers=True, is_assemblage=True)

class MarsFloraReferenceSample(MarsCollectionObject):
    """Flora Reference Sample
    DEPRECATED DELETED AND NOT USED"""
    schema = FloraRefSampleSchema

    portal_type = "Flora Reference Sample"
    archetype_name = "Flora Reference Sample"


registerType(MarsFloraRemain, PROJECTNAME)
registerType(MarsFloraIndividual, PROJECTNAME)
registerType(MarsFloraAssemblage, PROJECTNAME)
registerType(MarsFloraReferenceSample, PROJECTNAME)

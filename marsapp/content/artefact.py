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


ArtefactBurialSchema = BurialSchema.copy()
ArtefactBurialSchema['burial'].vocabulary = hominid_burial



ArtefactSchema = Schema((

    MarscatField('rawMaterials',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='composedBy',
        widget=MarscatWidget(label='Raw Materials',
            label_msgid='label_rawmaterials',
            description='Select the materials composing this item.',
            description_msgid='help_rawmaterials',
            domain='mars',
            startup_directory='/marscategories/raw-material',
            ),
        schemata='description',
        ),

    ))

ArtefactRemainSchema = MarsCollectionObjectSchema.copy()
ArtefactRemainSchema += PreservationSchema.copy()
ArtefactRemainSchema += CollectionObjectBaseSchema.copy()
ArtefactRemainSchema += BioOriginSchema.copy()
ArtefactRemainSchema += ArtefactBurialSchema.copy()
ArtefactRemainSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/artefact'
ArtefactRemainSchema['text'].widget.visible['view'] =  ArtefactRemainSchema['text'].widget.visible['edit'] = 'visible'


ArtefactRemainSchema += Schema((

    TextField('remainSubtype',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Subtype',
            label_msgid='label_archeoligical_subtype',
            description='Detailed Typological identification or precise types if it is a composite object.',
            description_msgid='help_archeological_subtype',
            domain='mars',
            ),
        schemata='description',
        ),

    ))

ArtefactRemainSchema += ArtefactSchema.copy()
ArtefactRemainSchema += ChronologySchema.copy()
ArtefactRemainSchema += ChronologyDatingSchema.copy()
ArtefactRemainSchema += TaphonomySchema.copy()
ArtefactRemainSchema += TechnologySchema.copy()
ArtefactRemainSchema += DiscoverySchema.copy()
ArtefactRemainSchema += AdministrationSchema.copy()
finalizeMarsSchema(ArtefactRemainSchema,multivalued=('remainType',), delFields=['discoverySite'], remain_types=ARTEFACTS_TYPES)

class MarsArtefact(MarsCollectionObject):
    """Artefact Remain"""
    schema = ArtefactRemainSchema

    portal_type = "Artefact"
    archetype_name = "Artefact"

ArtefactIndividualSchema = MarsCollectionObjectSchema.copy()
ArtefactIndividualSchema += PreservationSchema.copy()
ArtefactIndividualSchema += CollectionObjectBaseSchema.copy()
ArtefactIndividualSchema += ArtefactSchema.copy()
ArtefactIndividualSchema += BioOriginSchema.copy()
ArtefactIndividualSchema += AssemblageSchema.copy()
ArtefactIndividualSchema += ChronologySchema.copy()
ArtefactIndividualSchema += ChronologyDatingSchema.copy()
ArtefactIndividualSchema += TaphonomySchema.copy()
ArtefactIndividualSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/artefact'
ArtefactIndividualSchema += TechnologySchema.copy()
ArtefactIndividualSchema += DiscoverySchema.copy()
ArtefactIndividualSchema += AdministrationSchema.copy()
ArtefactIndividualSchema += ArtefactBurialSchema
finalizeMarsSchema(ArtefactIndividualSchema, multivalued=('remainType',),
                   delFields=('MNI', 'MNIDetermination', 'discoverySite',), remain_types=ARTEFACTS_TYPES)

class MarsArtefactIndividual(MarsCollectionObject):
    """Artefact Individual"""
    schema = ArtefactIndividualSchema

    portal_type = "Artefact Individual"
    archetype_name = "Artefact Individual"


ArtefactAssemblageSchema = MarsCollectionObjectSchema.copy()
ArtefactAssemblageSchema += CollectionObjectBaseSchema.copy()
ArtefactAssemblageSchema += ArtefactSchema.copy()
ArtefactAssemblageSchema += AssemblageSchema.copy()
ArtefactAssemblageSchema += BioOriginSchema.copy()
ArtefactAssemblageSchema += ChronologySchema.copy()
ArtefactAssemblageSchema += ChronologyDatingSchema.copy()
ArtefactAssemblageSchema += TaphonomySchema.copy()
ArtefactAssemblageSchema += TechnologySchema.copy()
ArtefactAssemblageSchema += DiscoverySchema.copy()
ArtefactAssemblageSchema += ArtefactBurialSchema.copy() 
ArtefactAssemblageSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/artefact'
ArtefactAssemblageSchema += AdministrationSchema.copy()
finalizeMarsSchema(ArtefactAssemblageSchema, igNumbers=True,
                    delFields=('igYear','discoverySite',), multivalued=('remainType',), remain_types=ARTEFACTS_TYPES)

class MarsArtefactAssemblage(MarsCollectionObject):
    """Artefact Assemblage"""
    schema = ArtefactAssemblageSchema

    portal_type = "Artefact Assemblage"
    archetype_name = "Artefact Assemblage"


RefSampleSchema = MarsCollectionObjectSchema.copy()
RefSampleSchema += CollectionObjectBaseSchema.copy()
RefSampleSchema += ChronologySchema.copy()
RefSampleSchema += AdministrationSchema.copy()
RefSampleSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/artefact'
RefSampleSchema += AssemblageSchema.copy()
finalizeMarsSchema(RefSampleSchema, igNumbers=True, delFields=['discoverySite'], remain_types=ARTEFACTS_TYPES)

class MarsReferenceSample(MarsCollectionObject):
    """Artefact Reference Sample"""
    schema = RefSampleSchema

    portal_type = "Reference Sample"
    archetype_name = "Reference Sample"


ArtefactRefSampleSchema = MarsCollectionObjectSchema.copy()
ArtefactRefSampleSchema += CollectionObjectBaseSchema.copy()
ArtefactRefSampleSchema += ArtefactSchema.copy()
ArtefactRefSampleSchema += ChronologySchema.copy()
ArtefactRefSampleSchema += AdministrationSchema.copy()
ArtefactRefSampleSchema += AssemblageSchema.copy()
ArtefactRefSampleSchema['remainType'].widget.startup_directory = '/marscategories/remain-type/artefact'
ArtefactRefSampleSchema += TechnologySchema.copy()
finalizeMarsSchema(ArtefactRefSampleSchema, delFields=['discoverySite'], remain_types=ARTEFACTS_TYPES, igNumbers=True)

class MarsArtefactReferenceSample(MarsCollectionObject):
    """Artefact Reference Sample"""
    schema = ArtefactRefSampleSchema

    portal_type = "Artefact Reference Sample"
    archetype_name = "Artefact Reference Sample"


registerType(MarsArtefact, PROJECTNAME)
registerType(MarsArtefactIndividual, PROJECTNAME)
registerType(MarsArtefactAssemblage, PROJECTNAME)
registerType(MarsReferenceSample, PROJECTNAME)
registerType(MarsArtefactReferenceSample, PROJECTNAME)

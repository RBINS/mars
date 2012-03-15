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

StructureAssemblageSchema = MarsCollectionObjectSchema.copy()
StructureAssemblageSchema += CollectionObjectBaseSchema.copy()
StructureAssemblageSchema += PreservationSchema.copy()
StructureAssemblageSchema += AssemblageSchema.copy()
StructureAssemblageSchema += ChronologySchema.copy()
StructureAssemblageSchema += ChronologyDatingSchema.copy()
StructureAssemblageSchema += TaphonomySchema.copy()
#StructureAssemblageSchema += TechnologySchema.copy()
StructureAssemblageSchema += DiscoverySchema.copy()
StructureAssemblageSchema += AdministrationSchema.copy()
StructureAssemblageSchema += InsiteLocationSchema.copy()
for k in 'remainType', 'discoverySite', 'discoveryPlace':
    if k in StructureAssemblageSchema:
        del StructureAssemblageSchema[k]
if StructureAssemblageSchema.has_key('stratigraphicalLayer'):
    StructureAssemblageSchema.moveField('stratigraphicalLayer', after='discoveryExcavation')

finalizeMarsSchema(StructureAssemblageSchema, igNumbers=True)

class MarsStructureAssemblage(MarsCollectionObject):
    """Structure Assemblage"""
    schema = StructureAssemblageSchema

    portal_type = "Structure Assemblage"
    archetype_name = "Structure Assemblage"


registerType(MarsStructureAssemblage, PROJECTNAME)

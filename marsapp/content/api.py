#-*- coding: utf-8 -*-
#  mars http://www.naturalsciences.be/metamars/products/
#  Archetypes implementation of the MARS core types based on ATContentTypes
#  Copyright (c) 2003-2006 MARS development team
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


from zope.interface import implementedBy, implements
from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import registerType as _rt
from Products.ATContentTypes.content.base import registerATCT as _rat
from Products.ATContentTypes.interface import IATDocument
from Products.ATContentTypes.atct import ATCTContent
from Products.ATContentTypes.atct import ATDocument
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.atct import ATBTreeFolder
from Products.ATContentTypes.atct import ATFile
from Products.ATContentTypes.atct import ATImage

from base import MarsCollectionObject

from interfaces import IFilesAndImagesContainer

registerATCT = _rat

def registerType(class_, project=None):
    _rt(class_, project)


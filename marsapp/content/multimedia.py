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
#from externalfile import MarsExternalFile
from config import PROJECTNAME


class MarsMediaAudioFile(ATFile):
    """Audio file"""

    portal_type = "Media File Audio"
    archetype_name = "Media File Audio"


class MarsMediaVideoFile(ATFile):
    """Video file"""

    portal_type = "Media File Video"
    archetype_name = "Media File Video"


class MarsMediaFlashFile(ATFile):
    """Flash file"""

    portal_type = "Media File Flash"
    archetype_name = "Media File Flash"


class MarsMediaObj3DFile(ATFile):
    """Obj3D file"""

    portal_type = "Media File 3D Object"
    archetype_name = "Media File 3D Object"


registerATCT(MarsMediaAudioFile, PROJECTNAME)
registerATCT(MarsMediaVideoFile, PROJECTNAME)
registerATCT(MarsMediaFlashFile, PROJECTNAME)
registerATCT(MarsMediaObj3DFile, PROJECTNAME)
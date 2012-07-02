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
A lot of code stolen from ATPhoto
"""
__author__  = 'David Convent <david.convent@naturalsciences.be>'
__docformat__ = 'restructuredtext'


from api import *
from config import PROJECTNAME
from schemata import *


MarsPictureSchema = ATImageSchema.copy()
MarsPictureSchema += AcquisitionSchema.copy()
MarsPictureSchema += AdministrationSchema.copy()
finalizeATCTSchema(MarsPictureSchema)

class MarsPicture(ATImage):
    security = ClassSecurityInfo()
    #__implements__ = (getattr(ATImage,'__implements__',()),)

    schema = MarsPictureSchema

    portal_type = "Picture"
    archetype_name = "Picture"

    security.declarePrivate('setImage')
    def setImage(self, value, refresh_exif=True, refresh_iptc=True, **kwargs):
#        self.getIPTC(value,refresh=refresh_iptc)
        self.getEXIF(value, refresh=refresh_exif)
        self._setATCTFileContent(value, **kwargs)

    security.declarePublic('getMimeType')
    def getMimeType(self):
        return self.lookupMime(self.get_content_type())

    security.declarePublic('getSizes')
    def getSortedSizes(self):
        field = self.getField('image')
        decorated = [ (i[1][0], i[0])
                      for i in field.getAvailableSizes(self).items() ]
        decorated.sort()
        sizes = [ size[1] for size in decorated]
        sizes.append('full')
        return sizes

    security.declarePublic('getSizes')
    def getSizes(self):
        field = self.getField('image')
        sizes = field.getAvailableSizes(self).keys()
        sizes.append('full')
        return sizes

    security.declarePublic('getWidth')
    def getWidth(self, scale=None):
        if(scale!='full'):
            return self.getSize(scale)[0]
        else:
            return self.width

    security.declarePublic('getHeight')
    def getHeight(self, scale=None):
        if(scale!='full'):
            return self.getSize(scale)[1]
        else:
            return self.height

    security.declarePublic('getAvailableSizes')
    def getAvailableSizes(self):
        """return avalaible sizes from MarsPicture schema
        """
        field = MarsPictureSchema.get('image')
        return field.sizes

registerATCT(MarsPicture, PROJECTNAME)

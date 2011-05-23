# Inspiration taken from PloneRailroadVideoLibrary
from zope.interface import Interface, implements
from zope.interface.verify import verifyObject

from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import Schema, LinesField, LinesWidget
from Products.ATContentTypes.content.base import registerATCT
from Products.ATContentTypes.atct import ATFolder
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.CMFPlone.interfaces import IPloneSiteRoot

from field import getTitledPath
from storage import CAT_CONTAINER


BaseCategorySchema = ATFolderSchema.copy()

schema = BaseCategorySchema + Schema((
    LinesField('synonyms',
        searchable=True,
        widget=LinesWidget(description='Enter a value for synonyms.',
            description_msgid='help_synonyms',
            i18n_domain='videolibrary',
            label='Synonyms',
            label_msgid='label_synonyms',),
            ),
    ))

def getFullTitledPath(obj, titles=None):
    if titles is None: titles = list()
    if not hasattr(obj, 'getId') or not hasattr(obj, 'Title'):
        return ()
    if obj.getId() != CAT_CONTAINER:
        titles.insert(0, obj.Title())
        titles = getFullTitledPath(obj.aq_inner.aq_parent, titles)
    return tuple(titles)
    

class IMarsCategory(Interface):
    """A Category in the MARS categorization system"""

class MarsCategory(ATFolder):
    """A subject in the classification scheme"""

    implements(IMarsCategory)

    security = ClassSecurityInfo()

    portal_type = archetype_name = 'Mars Category'

    schema = schema

    def cats_path(self):
        return getFullTitledPath(self)


registerATCT(MarsCategory, 'marsapp.categories')

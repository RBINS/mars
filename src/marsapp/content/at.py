import logging
from five import grok
from zope.interface import implements
from Products.Archetypes.public import TextField as TF
from Products.Archetypes.public import ReferenceField as RF
from archetypes.schemaextender.field import ExtensionField
from Products.CMFBibliographyAT.interface import IBibliographicItem
from zope.component import adapts
from Products.CMFCore.permissions import ModifyPortalContent
from Products.Archetypes.atapi import RichWidget
from mars.skin.browser.interfaces import IThemeSpecific
from Products.ATContentTypes.configuration import zconf
from archetypes.schemaextender.interfaces import (
    ISchemaModifier,
    ISchemaExtender,
    IBrowserLayerAwareExtender,
    IOrderableSchemaExtender,)
from Products.Archetypes.interfaces.base import IBaseObject
from Products.ATContentTypes import ATCTMessageFactory as _
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from plone.app.folder.folder import IATUnifiedFolder
allowupload = zconf.ATDocument.allow_document_upload
logger = logging.getLogger('marsapp.content.at')


class ReferenceField(ExtensionField, RF):
    """A trivial field."""


class TextField(ExtensionField, TF):
    """A trivial field."""


class RefFolderFields(object):
    adapts(IATUnifiedFolder)
    implements(ISchemaExtender,
               IBrowserLayerAwareExtender,
               IOrderableSchemaExtender)
    layer = IThemeSpecific

    fields = [
        ReferenceField(
            'relatedItems',
            relationship='relatesTo',
            multiValued=True,
            isMetadata=True,
            languageIndependent=False,
            index='KeywordIndex',
            referencesSortable=True,
            keepReferencesOnCopy=True,
            write_permission=ModifyPortalContent,
            widget=ReferenceBrowserWidget(
                allow_search=True,
                allow_browse=True,
                allow_sorting=True,
                show_indexes=False,
                force_close_on_insert=True,
                label=_(u'label_related_items', default=u'Related Items'),
                description='',
                visible={'edit': 'visible', 'view': 'invisible'}
            )
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.
        """
        found = None
        for k in schematas.keys():
            sh = schematas[k]
            if 'relatedItems' in sh:
                found = sh.pop(sh.index('relatedItems'))
        if found is not None:
            for k in schematas.keys():
                sh = schematas[k]
                if 'subject' in sh:
                    sh.insert(sh.index('subject') + 1, found)
                    found = None
            if found is not None:
                sh['default'].append(found)
        return schematas

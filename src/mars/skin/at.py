from archetypes.schemaextender.field import ExtensionField
from Products.ATContentTypes import ATCTMessageFactory as _
from Products.Archetypes.Field import LinesField as LF
from Products.Archetypes.Widget import LinesWidget
from archetypes.schemaextender.interfaces import (
    ISchemaExtender,
    IOrderableSchemaExtender, )
from zope.interface import implements


class LinesField(ExtensionField, LF):
    pass


class ArticleReferenceKeywordsExtender(object):
    implements(ISchemaExtender,
               IOrderableSchemaExtender)

    fields = [
        LinesField(
            'keywords',
            searchable=1,
            required=0,
            languageIndependent=1,
            is_duplicates_criterion=False,
            multiValued=1,
            widget=LinesWidget(
               label=_(u'label_keywords', default=u'Keywords'),
               description=_(u'help_keywords',
                             default=u'Categorization of the publications content.'),
               i18n_domain="cmfbibliographyat",
            ),
       ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields

    def getOrder(self, schematas):
        """ Manipulate the order in which fields appear.
        """
        for k in schematas.keys():
            sh = schematas[k]
            if 'keywords' in sh:
                if 'identifiers' in sh:
                    keyword = sh.pop(sh.index('keywords'))
                    sh.insert(sh.index('identifiers') + 1, keyword)
                else:
                    sh.append(sh.pop(sh.index('keywords')))
                schematas[k] = sh
        return schematas

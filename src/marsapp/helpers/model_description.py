# #-*- coding: utf-8 -*-
###############################################################################
# $Copy$
###############################################################################
""" Description view for the MARS Data Model

$Id$
"""
__docformat__ = 'reStructuredText'

# python imports
import logging

# zope2 imports
from Products.CMFCore.utils import getToolByName

# zope3 imports
from zope.interface import Interface
from zope.interface import implements

from marsapp.categories.storage import CAT_CONTAINER
from getTypeSchemas import getSchemas as printout

from Products.ATContentTypes.content.document import ATDocument
from Products.ATContentTypes.content.event import ATEvent
from Products.ATContentTypes.content.favorite import ATFavorite
from Products.ATContentTypes.content.file import ATFile
from Products.ATContentTypes.content.folder import ATFolder, ATBTreeFolder
from Products.ATContentTypes.content.image import ATImage
from Products.ATContentTypes.content.link import ATLink
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.ATContentTypes.content.topic import ATTopic

ATCTCLASSES = (
    ATDocument,
    ATEvent,
    ATFavorite,
    ATFile,
    ATFolder, ATBTreeFolder,
    ATImage,
    ATLink,
    ATNewsItem,
    ATTopic,
    )

from marsapp.content.analysis import MarsAnalysis, MarsAnalysisAbsoluteDating, MarsAnalysisRelativeDating
from marsapp.content.artefact import MarsArtefact, MarsArtefactIndividual, MarsArtefactAssemblage
from marsapp.content.collection import MarsCollection
from marsapp.content.curation import MarsCuration
from marsapp.content.excavation import MarsExcavation
from marsapp.content.fauna import MarsFaunaRemain, MarsFaunaIndividual, MarsFaunaAssemblage, MarsFaunaReferenceSample
from marsapp.content.flora import MarsFloraRemain, MarsFloraIndividual, MarsFloraAssemblage, MarsFloraReferenceSample
from marsapp.content.hominid import MarsHominidRemain, MarsHominidIndividual, MarsHominidAssemblage, MarsHominidReferenceSample
from marsapp.content.institution import MarsInstitution
from marsapp.content.people import MarsPeople
from marsapp.content.site import MarsSite
from marsapp.content.stratigraphy import MarsStratigraphy, MarsStratigraphicalLayer
from marsapp.content.structure import MarsStructureAssemblage
#from marsapp.content.externalfile import MarsExternalFile
#from marsapp.content.multimedia
#import picture

MARSCLASSES = (
    MarsPeople,
    MarsInstitution,
    MarsCuration,
    MarsSite,
    MarsExcavation,
    MarsStratigraphy, MarsStratigraphicalLayer,
    MarsCollection,
    MarsArtefact, MarsArtefactIndividual, MarsArtefactAssemblage,
    MarsFaunaRemain, MarsFaunaIndividual, MarsFaunaAssemblage, MarsFaunaReferenceSample,
    MarsFloraRemain, MarsFloraIndividual, MarsFloraAssemblage, MarsFloraReferenceSample,
    MarsHominidRemain, MarsHominidIndividual, MarsHominidAssemblage, MarsHominidReferenceSample,
    MarsStructureAssemblage,
    MarsAnalysis, MarsAnalysisAbsoluteDating, MarsAnalysisRelativeDating,
#    from marsapp.content.externalfile import MarsExternalFile
#    from marsapp.content.multimedia
#    import picture
    )

from Products.CMFBibliographyAT.content.folder import BibliographyFolder, LargeBibliographyFolder
from Products.CMFBibliographyAT.content.article import ArticleReference
from Products.CMFBibliographyAT.content.book import BookReference
from Products.CMFBibliographyAT.content.booklet import BookletReference
from Products.CMFBibliographyAT.content.conference import ConferenceReference
from Products.CMFBibliographyAT.content.inbook import InbookReference
from Products.CMFBibliographyAT.content.incollection import IncollectionReference
from Products.CMFBibliographyAT.content.inproceedings import InproceedingsReference
from Products.CMFBibliographyAT.content.manual import ManualReference
from Products.CMFBibliographyAT.content.mastersthesis import MastersthesisReference
from Products.CMFBibliographyAT.content.misc import MiscReference
from Products.CMFBibliographyAT.content.phdthesis import PhdthesisReference
from Products.CMFBibliographyAT.content.preprint import PreprintReference
from Products.CMFBibliographyAT.content.proceedings import ProceedingsReference
from Products.CMFBibliographyAT.content.techreport import TechreportReference
from Products.CMFBibliographyAT.content.unpublished import UnpublishedReference
from Products.CMFBibliographyAT.content.webpublished import WebpublishedReference
from Products.CMFBibliographyAT.content.pdf import PdfFolder, PdfFile

BIBLIOCLASSES = (
    BibliographyFolder, LargeBibliographyFolder,
    ArticleReference,
    BookReference,
    BookletReference,
    ConferenceReference,
    InbookReference,
    IncollectionReference,
    InproceedingsReference,
    ManualReference,
    MastersthesisReference,
    MiscReference,
    PhdthesisReference,
    PreprintReference,
    ProceedingsReference,
    TechreportReference,
    UnpublishedReference,
    WebpublishedReference,
    PdfFolder, PdfFile,
    )

ALLCLASSES = ATCTCLASSES + MARSCLASSES

from Products.Five.browser import BrowserView

EXCLUDE_SCHEMATA = ('metadata')

def getFieldAttributes(field):
    return result

from config import FTI_STUFF

class MarsModelView(BrowserView):
    """
    """

    @property
    def model_as_dicts(self):
        return self.model_as_dicts_for_klasses(MARSCLASSES)

    def model_as_dicts_for_klasses(self, klasses):
        pt = getToolByName(self.context, 'portal_types')
        result = list()
        for klass in klasses:
            values = dict()
            obj = klass('object_id')
            # Initialize some values we'll need later
            values['contained_in'] = list()

            # Extract basic class attributes
            values['klass'] = dict()
            values['klass']['name'] = klass.__name__
            values['klass']['meta_type'] = klass.meta_type
            values['klass']['portal_type'] = klass.portal_type
            values['klass']['archetype_name'] = klass.archetype_name

            # Extract Factory Type Info
            fti = pt.getTypeInfo(obj)
            values['fti'] = dict()
            values['fti']['id'] = fti.getId(),
            values['fti']['title'] = fti.Title()
            values['fti']['description'] = fti.description
            values['fti']['content_icon'] = fti.content_icon
            values['fti']['content_meta_type'] = fti.content_meta_type
            values['fti']['factory'] = fti.factory
            values['fti']['global_allow'] = fti.global_allow
            values['fti']['filter_content_types'] = fti.filter_content_types
            values['fti']['allowed_content_types'] = [
                {'name': t,} for t in fti.allowed_content_types
                ]
            values['fti']['allow_discussion'] = fti.allow_discussion
            values['fti']['immediate_view'] = fti.immediate_view
            values['fti']['default_view'] = fti.default_view
            values['fti']['default_view_fallback'] = fti.default_view_fallback
#            values['fti']['listActions'] = fti.listActions()

            # 'Build' the schema
            schematas = list()
            schemata_names = [ s for s in obj.schema.getSchemataNames()
                               if s not in EXCLUDE_SCHEMATA ]
            for schemata_name in schemata_names:
                schemata = dict()
                schemata['name'] = schemata_name
                schemata['fields'] = list()
                for field in obj.Schema().filterFields(schemata=schemata_name):
                    fieldattrs = {
                        'id': field.__name__,
                        'name': field.getName(),
                        'type': field.type,
                        'required': bool(field.required),
                        'default': field.default,
                        'default_method': field.default_method \
                                          and str(field.default_method) \
                                          or None,
                        'vocabulary': field.vocabulary,
                        'enforceVocabulary': bool(field.enforceVocabulary) \
                                             or False,
                        'multivalued': bool(field.multiValued),
                        'searchable': bool(field.searchable),
                        'isMetadata': bool(field.isMetadata),
                        'accessor': field.accessor,
                        'edit_accessor': field.edit_accessor,
                        'mutator': field.mutator,
                        'mode': field.mode,
                        'read_permission': field.read_permission,
                        'write_permission': field.write_permission,
                        'storage': field.storage.getName(),
#                        'generateMode': field.generateMode,
#                        'force': field.force,
                        'category_path': hasattr(field, 'getStartupDirectory') \
                                      and field.getStartupDirectory(obj) or None,
                        'widget': {
                            'name': field.widget.getName(),
                            'label': field.widget.label,
                            'description': field.widget.description,
                            'visible': field.widget.visible,
##            if hasattr(field.widget, 'domain'):
##                domain = field.widget.domain
##            else:
##                domain = 'plone'
##            if hasattr(field.widget, 'label_msgid'):
##                printout(out, '          widget label msg_id: %s' \
##                                                    %field.widget.label_msgid)
##                printout(out, '          widget label (fr): %s' \
##                            %utranslate(domain,
##                                        field.widget.label_msgid,
##                                        target_language='fr'))
                            },
#                        'validators': str(field.validators),
#                        'index': field.index,
#                        'index_method': field.index_method,
#                        'languageIndependent': field.languageIndependent,
                        }
                    schemata['fields'].append(fieldattrs)
                schematas.append(schemata)
            values['schematas'] = tuple(schematas)
            result.append(values)

        # Now we need to complete container_for and contained_in info
        for klass in result:
            for act in klass['fti']['allowed_content_types']:
                for cklass in result:
                    if cklass['klass']['portal_type'] == act['name']:
                        act['klassname'] = cklass['klass']['name']
                        act['display'] = act['name']
                        if cklass['fti']['title'] != act['name']:
                            act['display'] += " (%s)" %cklass['fti']['title']
                        cii = {
                            'klassname': klass['klass']['name'],
                            'display': klass['klass']['portal_type'],
                            }
                        if klass['klass']['portal_type'] != klass['fti']['title']:
                            cii['display'] += " (%s)" %klass['fti']['title']
                        cklass['contained_in'].append(cii)

        # We're done
        return result

class CompleteModelView(MarsModelView):
    """
    """

    def __repr__(self):
        self.request.response.setHeader("Content-Type", "text/plain")
        records = self.model_as_dicts
#        rec = records[9]
        return str(records)

    def model_as_dicts_for_klasses(self, klasses):
        from cStringIO import StringIO
        out = StringIO()
        pt = getToolByName(self.context, 'portal_types')

        for klass in klasses:
            obj = klass('object_id')
            # 'Build' the schema
            print >> out, klass.portal_type
            schema = list()
            for field in obj.Schema().fields():
                print >> out, "  %s (%s) - %s" % (field.getName(), str(field.type), field.widget.getName())
            print >> out, ''

        return out.getvalue()


    @property
    def model_as_dicts(self):
        return self.model_as_dicts_for_klasses(ALLCLASSES)


class IMarsModelDescription(Interface):
    """ Interface for MARS Model description generator
    """

class MarsModelDescriptionView(object):
    """ A view
    """

    implements(IMarsModelDescription)

    def __init__(self, context, request):
        self.context = getattr(context, CAT_CONTAINER)
        self.request = request
        self.catalog = getToolByName(self.context, 'portal_catalog')

    def __call__(self):
        return printout(self.context)

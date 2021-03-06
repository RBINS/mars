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
__docformat__ = 'restructuredtext'


import re
from DateTime import DateTime
import datetime

try:
  from Products.LinguaPlone.public import *
except ImportError:
  # No multilingual support
  from Products.Archetypes.public import *

from marsapp.categories.widget import ReferenceBrowserWidget

from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from plone.formwidget.datetime.at import DateWidget, DatetimeWidget, YearWidget
from Products.ATContentTypes.content.folder import ATFolderSchema
from Products.ATContentTypes.content.folder import ATBTreeFolderSchema
from Products.ATContentTypes.content.file import ATFileSchema
from Products.ATContentTypes.content.image import ATImageSchema
from Products.ATContentTypes.content.document import ATDocumentSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

#from Products.ExternalStorage.ExternalStorage import ExternalStorage

from Products.ATExtensions.field import RecordField
from Products.ATExtensions.widget import RecordWidget

from vocabularies import *
from field import CoordinatesField

from marsapp.categories.field import MarscatField
from marsapp.categories.widget import MarscatWidget

from marsapp.content.permissions import VIEW_REPOSITORY_PERMISSION
from marsapp.content.permissions import EDIT_REPOSITORY_PERMISSION

from marsapp.content import MarsMessageFactory as _

from Products.ATContentTypes.content.schemata import relatedItemsField


from ordereddict import OrderedDict

MarsBaseSchema = ATContentTypeSchema.copy()
MarsFolderSchema = ATFolderSchema.copy()
MarsBTreeFolderSchema = ATBTreeFolderSchema.copy()
MarsContentTypeSchema = ATFolderSchema.copy()
MarsCollectionObjectSchema = ATDocumentSchema.copy() + Schema((
#     ReferenceField('colRelatedSite',
#        required=False,
#        searchable=True,
#        multiValued=False,
#        relationship='colRelatedSite',
#        allowed_types=('Mars Site',),
#        widget=ReferenceBrowserWidget(label='Mars Site',
#            label_msgid='label_discovery_site',
#            description='Select the site related to this object',
#            description_msgid='help_discovery_site',
#            domain='mars',
#            startup_directory='/collections/sites',
#            ),
#        schemata='description',
#        ),

#        BooleanField('displayImages',
#            default=False,
#            languageIndependent=0,
#            widget=BooleanWidget(
#                description="If selected, a list of uploaded images will be "
#                             "presented at the bottom of the document to allow "
#                             "them to be easily downloaded.",
#                description_msgid='RichDocument_help_displayImages',
#                i18n_domain='richdocument',
#                label="""Display images download box""",
#                label_msgid='RichDocument_label_displayImages',
#            ),
#        ),
#
#        BooleanField('displayAttachments',
#            default=True,
#            languageIndependent=0,
#            widget=BooleanWidget(
#                description="If selected, a list of uploaded attachments will be "
#                             "presented at the bottom of the document to allow "
#                             "them to be easily downloaded",
#                description_msgid='RichDocument_help_displayAttachments',
#                i18n_domain='richdocument',
#                label="""Display attachments download box""",
#                label_msgid='RichDocument_label_displayAttachments',
#            ),
#        ),
#
#        BooleanField('imageCaption',
#            required = False,
#            languageIndependent = True,
#            widget = BooleanWidget(
#                label= _(
#                    u'help_enable_image_caption',
#                    default=u'Enable image caption'),
#                description = _(
#                    u'help_enable_image_caption',
#                    default=u'If selected, this will show the first image as a caption at the top of the page.')
#            ),
#        ),

    ),)


for schema in (MarsBaseSchema, MarsFolderSchema,
               MarsBTreeFolderSchema, MarsContentTypeSchema):
    schema['title'].widget.label = "Name"
    schema['title'].widget.label_msgid = "label_name"

BodyTextField = ATDocumentSchema['text'].copy()
BodyTextField.widget.allow_file_upload = False

SEARCHABLE_FIELDS = (
    'title', #index
    'synonyms',
    'description', #index
    'text',
    'igNumber', 'igNumber', #index
    'igYear', #index
    'nature',
    'status', #index
    'preservation', #index
    'remainType', #index
    'remainSubtype',
    'measures',
#    'measuresFile',
    'features', #index
    'featuresFile',
    'rawMaterials', #index
    'chronologies', #index
    'chronologyDetails', #index
    'BPDating', #index
    'datingAssociation', #index
    'taphonomies', #index
    'taphonomyDetermination',
    'manufactureYear', #index
    'manufacturePreciseDate',
    'artisan', #index
    'technologies', #index
    'technologyDetails',
    'functionalDescription',
    'usageMarkers', #index
    'discoveryYear', #index
    'datePrecision', #index
    'discoveryPreciseDate',
    'discoverers', #index
    'stratigraphicalLayer', #index
    'discoverySite', #index
    'discoveryPlace', #index
    'discoveryExcavation', #index ?
    'discoveryDetails',
    'excavationCoordinates', #index
#    'insuranceValue',
    'legalProperty', #index
    'copyright', #index
    'curations', #index
    'repository', #index
    'preciseRepository',
#    'repositoryLink',
    'repositoryStatus', #index
    'repositoryConditions',
    )



def make_dating_analysis(schemata='chronology'):
    return ReferenceField(
        'absoluteDatings',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='isAbsoluteDating',
        allowed_types=(
            "Analysis Absolute Dating",
            "Analysis Relative Dating",
        ),
        widget=ReferenceBrowserWidget(
            label='Dating analyse(s)',
            label_msgid='label_absolute_datings',
            description='Select Dating analyse(s).',
            description_msgid='help_absolute_datings',
            startup_directory_method="getMarsSiteOrCol",
            domain='mars',
        ),
        schemata=schemata,
    )


def make_discovery_site(schemata='discovery'):
    return ReferenceField(
        'discoverySite',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='siteFrom',
        allowed_types=('Mars Site',),
        widget=ReferenceBrowserWidget(label='Site',
                                      label_msgid='label_discovery_site',
                                      description='Select the site where it was excavated from (as precisely as possible).',
                                      description_msgid='help_discovery_site',
                                      domain='mars',
                                      startup_directory='/collections/sites',
                                     ),
        schemata=schemata,
    )


def make_dating_analysis_schema(schemata='chronology'):
    return Schema((
        make_dating_analysis(schemata=schemata),
    ))



def make_coordinates_file(schemata='description'):
    return ReferenceField('coordinateFiles',
        required=False,
        searchable=False,
        relationship='hasCoordinatesFiles',
        allowed_types=FILE_TYPES,
        widget=ReferenceBrowserWidget(label='Coordinate File(s)',
            label_msgid='label_coordinate_files',
            description='Upload Coordinate File(s).',
            description_msgid='help_coordinate_files',
            startup_directory_method='getMarsColFiles',
            domain='mars',
            ),
        schemata=schemata,
        )

def make_coordinates_file_schema(schemata='description'):
    return Schema((
        make_coordinates_file(schemata=schemata),
    ))
def make_synonyms_field():
    return LinesField('synonyms',
                                   required=False,
                                   searchable=False,
                                   widget=LinesWidget(label='Alternate Names or IDs',
                                                      label_msgid='label_synonym_name',
                                                      description="Synonyms, different spellings or given names.",
                                                      description_msgid='help_synonym_name',
                                                      domain='mars',
                                                     ),
                                   schemata='default',
                                  )

def finalizeMarsSchema(schema,
                       folderish=False,
                       moveDiscussion=True,
                       addBodyText=True,
                       igNumbers=False,
                       delFields=(),
                       multivalued=(),
                       remain_types = None,
                       add_synonyms=False,
                       is_assemblage=False,
                       is_collection_object=False,
                      ):
    """Finalizes a Mars type schema to alter some fields
    """

    if addBodyText:
        schema.addField(BodyTextField)

    if igNumbers:
        if schema.has_key('igNumber'):
            schema.delField('igNumber')
        field = LinesField('igNumbers',
            required=False,
            searchable=False,
            widget=LinesWidget(
                description=_(u'help_IGs',
                              default=_(u'General inventorisation',
                                       u'numbers (one per line).')),
                label=_(u'label_IGs', default=u'IG numbers'),
                ),
            )
        schema.addField(field)
        if schema.has_key('igYear'):
            schema.moveField('igNumbers', before='igYear')

    if not 'synonyms' in schema.keys() and add_synonyms:
        schema.addField(make_synonyms_field())

    for fieldname in delFields:
        if schema.has_key(fieldname):
            schema.delField(fieldname)

    for fieldname in multivalued:
        schema[fieldname].multiValued = True


    if schema.has_key('displayImages'):
        schema.changeSchemataForField('displayImages', 'attachments')
    if schema.has_key('displayAttachments'):
        schema.changeSchemataForField('displayAttachments', 'attachments')
    if schema.has_key('imageCaption'):
        schema.changeSchemataForField('imageCaption', 'attachments')
    if remain_types and ('components' in schema):
        schema['components'].allowed_types = remain_types

    finalizeATCTSchema(schema, folderish, moveDiscussion)

    if schema.has_key('relatedItems'):
        #schema['relatedItems'].widget.visible['edit'] = 'visible'
        #schema['relatedItems'].widget.visible['view'] = 'visible'
        #schema['relatedItems'].widget.visible['edit'] = 'invisible'
        #schema['relatedItems'].widget.visible['view'] = 'hidden'
        schema['relatedItems'].widget = ReferenceBrowserWidget(
            allow_search = True,
            allow_browse = True,
            allow_sorting = True,
            show_indexes = False,
            force_close_on_insert = True,
            label = _(u'label_related_items', default=u'Related Items'),
            description = '',
            visible = {'edit' : 'visible', 'view' : 'invisible' }
        )


    if is_assemblage:
        if 'taxon' in schema.keys():
            schema['taxon'].multiValued = True

    if is_collection_object:
        if not 'discoverySite' in schema.keys():
            field = make_discovery_site(schemata='description')
            schema.addField(field)
            schema.changeSchemataForField('discoverySite', 'description')

    for key in schema.keys():
        field = schema[key]
        if hasattr(field, 'required'):
            field.required = False
        widget = field.widget

    for fieldname in SEARCHABLE_FIELDS:
        if schema.has_key(fieldname) \
        and bool(schema[fieldname].searchable) is not True:
            schema[fieldname].searchable = True


    order1 = OrderedDict([
        #('title',     {'after':[], 'before':[],},),
        ('synonmyms', {'after':["title"], 'before':[],},),
        ('text', {'after':["synonyms"], 'before':[],},),
        ('beginningYear', {'after':[], 'before':['endingYear'],},),
        ('endingYear', {'after':[], 'before':['preciseDate'],},),
        ('preciseDate', {'after':[], 'before':['siteType', 'remainType'],},),
        ('siteType', {'after':[],   'before':["description"],},),
        ('description', {'after':["siteType"],'before':[],},),
        ('detailedDescription', {'after':["description"],"before":[], },),
        ('country', {'after':["detailedDescription"], 'before':[],},),
        ('map', {'after':['county'],'before': [] },),
        ('location', {'after':["map"], 'before':[],},),
        ('gisCoordinates', {'after':['location'],'before': []},),
        ('gisPrecision', {'after':["gisCoordinates"], 'before':[],},),
        ('gisProjection', {'after':['gisPrecision'], 'before':[],},),
        ('coordinatesOthers', {'after':["gisProjection"], 'before': [],},),
        ('coordinateFiles', {'after':["coordinatesOthers"], 'before':[],},),
        ('extGeoMapping', {'after':["coordinateFiles"], 'before':[],},), 
        ('substratum', {'after':["insiteLocation"], 'before': [],},),
        ('stratigraphyEquivalents', {'after': ["substratum"], 'before':[],},),
        ('stratigraphyLayersComposition', {'after': ["stratigraphyEquivalents"], 'before': [],},),
        ('insiteLocation', {'after':["history"], 'before': [],},),
        ('excavators', {'after':['coordinateFiles'], 'before': [],},),
        ('excavationDetails', {'after':['excavators'], 'before': [],},),
        ('excavationMap', {'after':['excavationDetails'], 'before': [],},),
        ('chronomlogies', {'after':[], 'before': ['chronologyDetails'],},),
        ('chronologyDetails', {'after':[], 'before': ['BPDating'],},),
        ('BPDating', {'after': [], 'before': ['datingAssociation'],},),
        ('discoveryYear', {'after':[], 'before': ['datePrecision'],},),
        ('datePrecision', {'after':[], 'before': ['discoveryPreciseDate'],},),
        ('discoveryPreciseDate', {'after': [], 'before': ['discoverers'],},),
        ('discoverers', {'after':[], 'before': ['discoveryDetails'],},),
        ('coordinatesOthers', {'after':['gisProjection'], 'before':[],},),
        ('remainType', {'after':['status'], 'before':[],},),
        ('measures', {'after':['remainType'], 'before':[],},),
        ('measuresFile', {'after':['measures'], 'before':[],},),
        ('features', {'after':['measuresFile'], 'before':[],},),
        ('featuresFile', {'after':['features'], 'before':[],},),
        ('laterality:!', {'after':['featuresFile'], 'before':[],},),
        ('polarity', {'after':['laterality'], 'before':[],},),
        ('burial', {'after':['polarity'], 'before':[],},),
        ('burialDetermination', {'after':['burial'], 'before':[],},),
        ('rawMaterials', {'after':['burialDetermination'], 'before':[],},),
        ('origin', {'after':['rawMaterials'], 'before':[],},),
        ('originDetermination', {'after':['origin'], 'before':[],},),
        ('paleoecology', {'after':['originDetermination'], 'before':[],},),
        ('components', {'after':['howManyComponents'], 'before':[],},),
        ('componentsDistributionDesc', {'after':['components'], 'before':[],},),
        ('componentsDistributionFile', {'after':['componentsDistributionDesc'], 'before':[],},),
        ('attributionInfo', {'after':['componentsDistributionFile'], 'before':[],},),
        ('MNI', {'after':['componentsDistributionDesc'], 'before':[],},),
        ('MNIDetermination', {'after':['MNI'], 'before':[],},),
    ])
    #for k in order.keys():
    #    orders = order[k]
    #    for item in orders['before']:
    #        if not item in order:
    #            order[item] = {'after': [], 'before': []}
    #        if not k in order[item]['after']:
    #            order[item]['after'].append(k)
    #    for item in orders['after']:
    #        if not item in order:
    #            order[item] = {'after': [], 'before': []}
    #        if not item in order[item]['before']:
    #            order[item]['before'].append(k) 
            
    if schema.has_key('synonyms'):
        schema.moveField('synonyms', before='description')
    if schema.has_key('remainSubtype'):
        schema.moveField('remainSubtype', after='remainType')
    if schema.has_key('rawmaterials'):
        schema.moveField('rawmaterials', before='measures') 
    if schema.has_key('presentation'):
        schema.moveField('presentation', before='allowDiscussion')
    if schema.has_key('tableContents'):
        schema.moveField('tableContents', after='presentation')
    if (schema.has_key('datingAssociation')
        and schema.has_key('absoluteDatings')):
        schema.moveField('absoluteDatings', after='datingAssociation') 
    if schema.has_key("stratigraphicalLayer") and schema.has_key("discoveryExcavation"):
        schema.moveField("discoveryExcavation", after="stratigraphicalLayer") 
    keys = schema.keys()
    def reorder(order):
        for k in order:
            for o in order[k]:
                for field in order[k][o]:
                    op = 'before'
                    if o == 'before':
                        op = 'after'
                    op = o
                    kw = {op:field}
                    if field in keys and k in keys:
                        try:
                            schema.moveField(k, **kw)
                        except:
                            import pdb;pdb.set_trace()  ## Breakpoint ##
    reorder(order1)
    # second pass
    order2 = OrderedDict([
        ('map', {'after':["country"], 'before':[],},), 
    ])
    reorder(order2)

BodyTextSchema = Schema(( BodyTextField, ))

CollectionBaseSchema = Schema((

    make_synonyms_field(),

    StringField('igNumber',
        required=False,
        searchable=False,
        widget=StringWidget(
            description=_(u'help_IG',
                          default=u'General inventorisation number'),
            label=_(u'label_IG', default=u'IG number'),
            ),
        schemata='default',
        ),

    DateTimeField('igYear',
        required=False,
        searchable=False,
        widget=YearWidget(label='Year of Inventorisation',
            label_msgid='label_IG_date',
            description='Year this item got its IG number.',
            description_msgid='help_IG_date',
            domain='mars',
            years_range = (-300, 10),
            ),
        schemata='default',
        ),

    ))

CollectionObjectBaseSchema = CollectionBaseSchema.copy() + Schema((

    MarscatField('remainType',
        required=True,
        searchable=True,
        relationship='isRemainType',
        multiValued=True,
        widget=MarscatWidget(label='Type',
            label_msgid='label_remain_type',
            description='Type of this remain (as precisely as possible).',
            description_msgid='help_remain_type',
            domain='mars',
            startup_directory='/marscategories/remain-type',
            ),
        schemata='description',
        ),

    TextField('measures',
        required=False,
        searchable=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Measures',
            label_msgid='label_measures',
            description='Give the measures, and also the protocol used to get these measures.',
            description_msgid='help_measures',
            domain='mars',
            ),
        schemata='description',
        ),

    ReferenceField('measuresFile',
        required=False,
        searchable=False,
        relationship='hasMeasuresFile',
        allowed_types=FILE_TYPES,
        widget=ReferenceBrowserWidget(label='Measures file',
            label_msgid='label_measures_file',
            description='Upload a file with all measures in it.',
            description_msgid='help_measures_file',
            startup_directory_method='getMarsColFiles',
            domain='mars',
            ),
        schemata='description',
        ),

    TextField('features',
        required=False,
        searchable=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        widget=RichWidget(label='Features',
            label_msgid='label_measures',
            description='Features and their determination.',
            description_msgid='help_measures',
            domain='mars',
            ),
        schemata='description',
        ),

    ReferenceField('featuresFile',
        required=False,
        searchable=False,
        relationship='hasFeaturesFile',
        allowed_types=FILE_TYPES,
        widget=ReferenceBrowserWidget(label='Features file',
            label_msgid='label_feasures_file',
            description='Upload a file describing the item features.',
            description_msgid='help_feasures_file',
            startup_directory_method='getMarsColFiles',
            domain='mars',
            ),
        schemata='description',
        ),

    ))


RefSampleBonesSchema = Schema((

    MarscatField('bones',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='composedBy',
        widget=MarscatWidget(label='Bone Components',
            label_msgid='label_bones',
            description='Select the bones making up this reference sample.',
            description_msgid='help_bones',
            domain='mars',
            ),
        schemata='description',
        ),

    LinesField('boneDetails',
        searchable=True,
        required=False,
        widget=LinesWidget(label='Bone components details',
            label_msgid='label_bones_detail',
            description='Advanced description of the bones.',
            description_msgid='help_bones_details',
            domain='mars',
            ),
        schemata='description',
        ),

    ))

InsiteLocationSchema = Schema ((

    TextField('insiteLocation',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='In-site location',
            label_msgid='label_excavation_unit',
            description='Part of the site excavated.',
            description_msgid='help_excavation_unit',
            domain='mars',
            ),
        schemata='description',
        ),

))


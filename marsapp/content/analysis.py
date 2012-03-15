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

AnalysisSchema = MarsBaseSchema.copy()
AnalysisSchema['title'].widget.label="ID"
AnalysisSchema['title'].widget.label_msgid="label_analysis_id"
AnalysisSchema['title'].widget.description="Unique ID of the analysis."
AnalysisSchema['title'].widget.description_msgid="help_analysis_id"
AnalysisSchema += Schema((

    MarscatField('analysisType',
        required=True,
        searchable=False,
        relationship='hasType',
        widget=MarscatWidget(
            label='Analysing technique',
            label_msgid='label_analysis_type',
            description='Select the used technique to perform this analysis.',
            description_msgid='help_analysis_type',
            domain='mars',
            startup_directory='/marscategories/analyse-type',
            ),
        schemata="description",
        ),

    IntegerField('year',
        required=False,
        searchable=True,
        size=4,
        widget=IntegerWidget(
            label='Year of analysis',
            label_msgid='label_analysis_year',
            description='Choose the year when this analysis was performed.',
            description_msgid='help_analysis_year',
            domain='mars',
            ),
        ),

    ReferenceField('submittor',
        searchable=False,
        required=False,
        relationship='submittedBy',
        allow_browse=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Submittor',
            label_msgid='label_submittor',
            description='Person or institute which submitted the analysis.',
            description_msgid='help_analysis_submittor',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata="description",
        ),

    ReferenceField('laboratory',
        searchable=False,
        required=False,
        relationship='analyzedIn',
        allowed_types=('Institution',),
        widget=ReferenceBrowserWidget(label='Laboratory',
            label_msgid='label_laboratory',
            description='Institute where the laboratory of this analysis can be found.',
            description_msgid='help_analysis_laboratory',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata="description",
        ),

    ReferenceField('authors',
        searchable=False,
        required=False,
        multiValued=True,
        relationship='analyzedBy',
        allow_browse=True,
        allowed_types=PEOPLE_AND_INSTITUTION,
        widget=ReferenceBrowserWidget(label='Analysis Author(s)',
            label_msgid='label_analysis_author',
            description='People or insititution (if people are unknown) who made the analysis.',
            description_msgid='help_analysis_author',
            domain='mars',
            startup_directory='/administration/organisations',
            ),
        schemata="description",
        ),

    ReferenceField('referenceSamples',
        searchable=False,
        required=False,
        multiValued=True,
        relationship='hasReference',
        allowed_types=REFERENCE_SAMPLES,
        widget=ReferenceBrowserWidget(label='Sample(s)',
            label_msgid='label_reference_samples',
            description='Samples used in this analysis.',
            description_msgid='help_analysis_reference_sample',
            domain='mars',
            ),
        schemata="description",
        ),

    TextField('sampleAndContext',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),  
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Sample and context',
            label_msgid='label_sample_and_context',
            description='Description of the sample (id, quality, weigth)',
            description_msgid='help_reference_and_context',
            domain='mars',
            ),
        schemata="description",
        ),

    TextField('protocols',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',), 
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Sampling and analysis protocol(s)',
            label_msgid='label_analysis_protocols',
            description='Description of the sampling and analysis protocol.',
            description_msgid='help_analysis_protocols',
            domain='mars',
            ),
        schemata="description",
        ),

    # XXX: Why not a workflow ??
    StringField('AnalysisStatus',
        required=False,
        searchable=True,
        vocabulary=analysis_status,
        widget=SelectionWidget(label='Status',
            label_msgid='label_analysis_status',
            description='Publication status',
            description_msgid='help_analysis_status',
            domain='mars',
            ),
        schemata="description",
        ),

    TextField('results',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),  
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Result(s)',
            label_msgid='label_results',
            description='Neutral Results of the analysis provided by the Laboratory',
            description_msgid='help_analysis_result',
            domain='mars',
            ),
        schemata="description",
        ),

    TextField('originalComments',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),   
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Raw Comments',
            label_msgid='label_comments',
            description='Raw comments delivered by the laboratory which made the analysis',
            
            description_msgid='help_comments',
            domain='mars',
            ),
        schemata="description",
        ),

    TextField('moreInfo',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),    
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Further information',
            label_msgid='label_more_info',
            description='Additional information on the analysis.',
            description_msgid='help_analysis_more_info',
            domain='mars',
            ),
        schemata="description",
        ),

    MarscatField('analysisKeywords',
        required=False,
        searchable=False,
        multiValued=True,
        relationship='isCategorisedAs',
        widget=MarscatWidget(
            label='Keywords',
            label_msgid='label_keywords',
            description='general period (Oxygen Isotopic Stadium with unknown option)',
            description_msgid='help_analysis_keywords',
            domain='mars',
            ),
        schemata="description",
        ),

    LinesField('specializedKeywords',
        searchable=True,
        required=False,
        widget=LinesWidget(label='Specialised keywords',
            label_msgid='label_keywords_specialised',
            description='Very subject specific keywords.',
            description_msgid='help_keywords_specialised',
            domain='mars',
            ),
        schemata="description",
        ),

    ))

finalizeMarsSchema(AnalysisSchema)

class MarsAnalysis(ATCTContent, MarsMixin):
    """Analysis"""
    schema = AnalysisSchema

    portal_type = "Analysis"
    archetype_name = "Analysis"


AbsoluteDatingAnalysisSchema = AnalysisSchema.copy()
AbsoluteDatingAnalysisSchema += Schema((

    IntegerField('absoluteAge',
        required=True,
        searchable=True,
        widget=IntegerWidget(label='Absolute Age',
            label_msgid='label_absolute_age',
            description='Enter the age, numbers only',
            description_msgid='help_absolute_age',
            domain='mars',
            ),
        schemata="dating",
        ),

    IntegerField('deviationMin',
        required=True,
        searchable=False,
        widget=IntegerWidget(label='Standard deviation min',
            label_msgid='label_standard_deviation_min',
            description='Enter the Standard deviation min, numbers only.',
            description_msgid='help_standard_deviation_min',
            domain='mars',
            ),
        schemata="dating",
        ),

    IntegerField('deviationMax',
        required=True,
        searchable=False,
        widget=IntegerWidget(label='Standard deviation max',
            label_msgid='label_standard_deviation_max',
            description='Enter the Standard deviation max, numbers only.',
            description_msgid='help_standard_deviation_max',
            domain='mars',
            ),
        schemata="dating",
        ),

    StringField('calibrationSoftware',
        required=False,
        searchable=False,
        widget=StringWidget(
            label='Calibration software',
            label_msgid='label_calibration_software',
            description='',
            description_msgid='help_calibration_software',
            domain='mars',
            ),
        schemata="dating",
        ),

    StringField('calibrationCurve',
        required=False,
        searchable=False,
        widget=StringWidget(
            label='Calibration Curve',
            label_msgid='label_calibration_curve',
            description='',
            description_msgid='help_calibration_curve',
            domain='mars',
            ),
        schemata="dating",
        ),

    TextField('calibratedAge',
        searchable=True,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),     
        default_output_type='text/x-html-safe',
        widget=RichWidget(label='Calibrated Age',
            label_msgid='label_calibrated_age',
            description='',
            description_msgid='help_calibrated_age',
            domain='mars',
            ),
        schemata="dating",
        ),

    ))
finalizeMarsSchema(AbsoluteDatingAnalysisSchema)

class MarsAnalysisAbsoluteDating(MarsAnalysis):
    """Absolute Dating Analysis"""
    schema = AbsoluteDatingAnalysisSchema

    portal_type = "Analysis Absolute Dating"
    archetype_name = "Analysis Absolute Dating"


RelativeDatingAnalysisSchema = AnalysisSchema.copy()
RelativeDatingAnalysisSchema += Schema((

    IntegerField('relativeAge',
        required=True,
        searchable=True,
        widget=IntegerWidget(label='Relative Age',
            label_msgid='label_relative_age',
            description='Enter the relative age, numbers only',
            description_msgid='help_relative_age',
            domain='mars',
            ),
        schemata="dating",
        ),

    MarscatField('chronology',
        required=False,
        searchable=False,
        relationship='chronologicallyFits',
        widget=MarscatWidget(
            label='Chronology',
            label_msgid='label_ois_chronology',
            description='general period (Oxygen Isotopic Stadium with unknown option)',
            description_msgid='help_ois_chronology',
            startup_directory='/marscategories/chronology',
            domain='mars',
            ),
        schemata="dating",
        ),

    TextField('chronologyDetails',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/plain',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Chronology Details',
            label_msgid='label_chronology_details',
            description='General chronology information',
            description_msgid='help_chronology_details',
            domain='mars',
            ),
        schemata="dating",
        ),

#    MarscatField('culturalChronology',
#        required=False,
#        searchable=False,
#        relationship='chronologicallyFits',
#        widget=MarscatWidget(label='Cultural Chrononlogy',
#            label_msgid='label_cultural_chronology',
#            description='Select the general Culture that this item belongs to.',
#            description_msgid='help_cultural_chronology',
#            domain='mars',
#            ),
#        schemata="dating",
#        ),

    TextField('ageDetermination',
        searchable=False,
        required=False,
        #default_content_type='text/plain',
        #allowable_content_types=('text/plain',),
        default_output_type='text/x-html-safe',
        allowable_content_types = ('text/plain',
                                  'text/structured',
                                  'text/html',),      
        widget=RichWidget(label='Age Determination',
            label_msgid='label_age_determination',
            description='General age information',
            description_msgid='help_age_determination',
            domain='mars',
            ),
        schemata="dating",
        ),

#    TextField('paleontologicalAge',
#        searchable=False,
#        required=False,
#        default_content_type='text/plain',
#        allowable_content_types=('text/plain',),
#        default_output_type='text/x-html-safe',
#        widget=TextAreaWidget(label='Paleontological Age',
#            label_msgid='label_paleontological_age',
#            description='Relative cultural age based on the fauna',
#            description_msgid='help_paleontological_age',
#            domain='mars',
#            ),
#        schemata="dating",
#        ),

#    TextField('geologicalAge',
#        searchable=False,
#        required=False,
#        default_content_type='text/plain',
#        allowable_content_types=('text/plain',),
#        default_output_type='text/x-html-safe',
#        widget=TextAreaWidget(label='Geological Age',
#            label_msgid='label_geological_age',
#            description='Relative cultural age based on the Stratigraphy',
#            description_msgid='help_geological_age',
#            domain='mars',
#            ),
#        schemata="dating",
#        ),

#    TextField('taphonomicalAge',
#        searchable=False,
#        required=False,
#        default_content_type='text/plain',
#        allowable_content_types=('text/plain',),
#        default_output_type='text/x-html-safe',
#        widget=TextAreaWidget(label='Taphonomical Age',
#            label_msgid='label_taphonomical_age',
#            description='Relative age based on the Taphonomic processes',
#            description_msgid='help_taphonomical_age',
#            domain='mars',
#            ),
#        schemata="dating",
#        ),

    ))
finalizeMarsSchema(RelativeDatingAnalysisSchema)

class MarsAnalysisRelativeDating(MarsAnalysis):
    """Relative Dating Analysis"""
    schema = RelativeDatingAnalysisSchema

    portal_type = "Analysis Relative Dating"
    archetype_name = "Analysis Relative Dating"


registerATCT(MarsAnalysis, PROJECTNAME)
registerATCT(MarsAnalysisAbsoluteDating, PROJECTNAME)
registerATCT(MarsAnalysisRelativeDating, PROJECTNAME)

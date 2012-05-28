# -*- coding: utf-8 -*-

import os, sys

from DateTime import DateTime
import datetime
import logging
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base as BTreeFolder
from Acquisition import aq_base
from marsapp.content.schemata.base import REFERENCEFIELDS_INDEXES

try:
    from Products.CMFPlone.migrations import migration_util
except:
    #plone4
    from plone.app.upgrade import utils as migration_util

from Products.CMFCore.utils import getToolByName


from Products.Archetypes.Field import StringField, IntegerField

from pprint import pprint
import transaction
from marsapp.content.schemata.vocabularies import REFERENCE_SAMPLES, DISCOVERY_PLACES

def upgrade(portal_setup):
    """
    """
    l = logging.getLogger('mars/policy/migrations/v29')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    request = site.REQUEST
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site, 'profile-Products.PloneSurvey:default')
    #migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v29:28-29')
    #portal_setup.runImportStepFromProfile('profile-collective.zipfiletransport:default', 'actions')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'catalog', run_dependencies=False)
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'jsregistry', run_dependencies=False)
    #portal_setup.runImportStepFromProfile('profile-marsapp.csvreplicata:default', 'mars_csvreplicata', run_dependencies=False)
    #portal_setup.runAllImportStepsFromProfile('profile-collective.js.datatables:default')
    #portal_setup.runAllImportStepsFromProfile('profile-plone.formwidget.datetime:default')
    #portal_setup.runAllImportStepsFromProfile('profile-collective.ckeditor:default')
    portal_setup.runAllImportStepsFromProfile('profile-collective.bibliocustomviews:default')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    ### reindex new indexes
    #for i in catalog.indexes():
    #    if not i in indexes:
    #        l.error('Reindexing %s' % i)
    #        catalog.reindexIndex(i, request)

    # migrate fields to datetimefields

    #cindexes = catalog.Indexes.objectIds()
    #ref_indexes = []
    #for a in REFERENCEFIELDS_INDEXES:
    #    for c in REFERENCEFIELDS_INDEXES[a]:
    #        if (not c in ref_indexes) and (c in cindexes):
    #            ref_indexes.append(c)
    #llen = len(ref_indexes)
    #for i, index in enumerate(ref_indexes):
    #    l.error('Reindexing %s (%s/%s)' % (index, 1+i, llen))
    #    catalog.reindexIndex(index, request)
    #portal_setup.runAllImportStepsFromProfile('profile-eea.facetednavigation:default')

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
from marsapp.content.interfaces import IMarsObject

def upgrade(portal_setup):
    """
    """
    l = logging.getLogger('mars/policy/migrations/v29')
    portal = site = portal_setup.aq_parent
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
    #portal_setup.runAllImportStepsFromProfile('profile-collective.bibliocustomviews:default')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    ### reindex new indexes
    class extra:
        index_type="Okapi BM25 Rank"
        lexicon_id="plone_lexicon"
    for k, tp, extra in  [
        ('cats_path', 'ZCTextIndex', extra),
     ]:
         if not k in catalog.Indexes:
             l.error('Creating %s in catalog' % k)
             catalog.addIndex(k, tp, extra)
             if not k in catalog._catalog.schema.keys():
                 catalog.addColumn(k)
             catalog.reindexIndex(k, portal.REQUEST)
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    brains = catalog.searchResults(
        object_provides=IMarsObject.__identifier__
    )
    indexes = []
    for a in REFERENCEFIELDS_INDEXES:
        for b in REFERENCEFIELDS_INDEXES[a]:
            if not b in indexes:
                indexes.append(b)
    lbrains = len(brains)
    l.error('Reindex %s' % indexes)
    for i, item in enumerate(brains):
        l.error('Reindex %s (%s/%s)' % (item.getPath(),  i, lbrains))
        item.getObject().reindexObject(indexes)



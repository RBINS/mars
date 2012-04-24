# -*- coding: utf-8 -*-

import os, sys

from DateTime import DateTime
import datetime
import logging
from Products.BTreeFolder2.BTreeFolder2 import BTreeFolder2Base as BTreeFolder
from Acquisition import aq_base

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
    l = logging.getLogger('mars/policy/migrations/v21')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    request = site.REQUEST
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site, 'profile-Products.PloneSurvey:default')
    #migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v21:20-21')
    #portal_setup.runImportStepFromProfile('profile-collective.zipfiletransport:default', 'actions')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'catalog', run_dependencies=False)
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    #portal_setup.runAllImportStepsFromProfile('profile-collective.js.datatables:default')
    mtypes = tuple(REFERENCE_SAMPLES) + tuple(DISCOVERY_PLACES) + ("Collection",)

    for item in catalog.searchResults(**{'portal_type': mtypes}):
        def migrate(obj, index):
            value = obj.getField(index).getAccessor(obj)()
            if isinstance(value, int):
                try:
                    dvalue = DateTime(
                    datetime.datetime(value, 1, 1))
                except:
                    dvalue = None

                obj.getField(index).getMutator(obj)(dvalue)

        obj = item.getObject()
        k = obj.schema.keys()
        indexes = ['discoveryYear', 'igYear', 'BPDating']
        for i in indexes:
            if i in k:
                l.error('Migrating %s / %s' % (
                    '/'.join(obj.getPhysicalPath()),
                    i
                ))
                migrate(obj, i)
    portal_setup.runAllImportStepsFromProfile('profile-plone.formwidget.datetime:default')
    ## reindex new indexes
    #for i in catalog.indexes():
    #    if not i in indexes:
    #        l.error('Reindexing %s' % i)
    #        catalog.reindexIndex(i, request)

    # migrate fields to datetimefields


    #portal_setup.runAllImportStepsFromProfile('profile-eea.facetednavigation:default')
                


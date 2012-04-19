# -*- coding: utf-8 -*-

import os, sys
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


def upgrade(portal_setup):
    """
    """
    l = logging.getLogger('mars/policy/migrations/v20')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    request = site.REQUEST
    indexes =  catalog.indexes()
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site, 'profile-Products.PloneSurvey:default')
    #migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v20:19-20')
    #portal_setup.runImportStepFromProfile('profile-collective.zipfiletransport:default', 'actions')
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'catalog', run_dependencies=False)
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    ##portal_setup.runAllImportStepsFromProfile('profile-collective.js.datatables:default')
    ## reindex new indexes
    catalog.refreshCatalog()
    #for i in catalog.indexes():
    #    if not i in indexes:
    #        l.error('Reindexing %s' % i)
    #        catalog.reindexIndex(i, request)

    #portal_setup.runAllImportStepsFromProfile('profile-eea.facetednavigation:default')
                


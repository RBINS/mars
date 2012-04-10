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



def upgrade(portal_setup):
    """
    """
    l = logging.getLogger('mars/policy/migrations/v17')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site,
    #                                    'profile-Products.PloneSurvey:default')
    #migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v17:16-17')
    #portal_setup.runImportStepFromProfile('profile-collective.zipfiletransport:default', 'actions')
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    #portal_setup.runAllImportStepsFromProfile('profile-collective.js.datatables:default')



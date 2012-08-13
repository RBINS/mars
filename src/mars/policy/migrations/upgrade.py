
# -*- coding: utf-8 -*-

import os, sys

try:
    from Products.CMFPlone.migrations import migration_util
except:
    #plone4
    from plone.app.upgrade import utils as migration_util

from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IATImage
from Products.ATContentTypes.content.image import ATImage
import transaction


import logging

log = logging.getLogger('mars migrations')

def css_upgrade(portal_setup):
    portal = site = portal_setup.aq_parent
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'cssregistry', run_dependencies=False)
    transaction.commit()
    log.warn('Css upgraded')

def js_upgrade(portal_setup):
    portal = site = portal_setup.aq_parent
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'jsregistry', run_dependencies=False)
    transaction.commit()
    log.warn('Js upgraded')

def recook_resources(portal_setup):
    portal = site = portal_setup.aq_parent
    jsregistry = getToolByName(site, 'portal_javascripts')
    cssregistry = getToolByName(site, 'portal_css')
    jsregistry.cookResources()
    cssregistry.cookResources()
    transaction.commit()
    log.warn('Recooked resources (js/css)')

def v1000(portal_setup):
    """
    """
    portal = site = portal_setup.aq_parent
    qi = site.portal_quickinstaller
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site,
    #                                    'profile-Products.PloneSurvey:default')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'jsregistry', run_dependencies=False)
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'cssregistry', run_dependencies=False)
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'portlets', run_dependencies=False)
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'propertiestool', run_dependencies=False)

    qi.reinstallProducts(
        [
            'collective.js.jqueryui',
            'eea.facetednavigation',
            'collective.js.datatables'
        ],)


    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'propertiestool', run_dependencies=False)
    transaction.commit()
    log.warn('Upgrade v1000 runned.')

def v1003(portal_setup):
    """
    """
    portal = site = portal_setup.aq_parent
    qi = site.portal_quickinstaller
    pm = portal.portal_migration
    report = pm.upgrade(dry_run=False)
    transaction.commit()
    log.warn('Upgrade v1003 runned.')

def v1004(portal_setup):
    """
    """
    portal = site = portal_setup.aq_parent
    qi = site.portal_quickinstaller
    pm = portal.portal_migration
    qi.reinstallProducts(
        [
            'plone.app.dexterity',
        ],)

    transaction.commit()
    log.warn('Upgrade v1004 runned.')

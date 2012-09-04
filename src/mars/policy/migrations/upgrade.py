
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
PROFILEIDS = 'mars.policy:z_mars_plone'
PROFILEID = 'profile-%s' % PROFILEIDS
TPROFILEIDS = 'mars.policy:default'
TPROFILEID = 'profile-%s' % PROFILEIDS

def css_upgrade(portal_setup):
    portal = site = portal_setup.aq_parent
    portal_setup.runImportStepFromProfile(PROFILEID, 'cssregistry', run_dependencies=False)
    transaction.commit()
    log.warn('Css upgraded')

def js_upgrade(portal_setup):
    portal = site = portal_setup.aq_parent
    portal_setup.runImportStepFromProfile(PROFILEID, 'jsregistry', run_dependencies=False)
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
    #portal_setup.runImportStepFromProfile(PROFILEID, 'jsregistry', run_dependencies=False)
    #portal_setup.runImportStepFromProfile(PROFILEID, 'cssregistry', run_dependencies=False)
    #portal_setup.runImportStepFromProfile(PROFILEID, 'portlets', run_dependencies=False)
    #portal_setup.runImportStepFromProfile(PROFILEID, 'propertiestool', run_dependencies=False)

    qi.reinstallProducts(
        [
            'collective.js.jqueryui',
            'eea.facetednavigation',
            'collective.js.datatables'
        ],)


    #portal_setup.runImportStepFromProfile(PROFILEID, 'propertiestool', run_dependencies=False)
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

def v1005(portal_setup):
    """
    """
    portal = site = portal_setup.aq_parent
    qi = site.portal_quickinstaller
    pm = portal.portal_migration
    transaction.commit()
    portal_setup.runAllImportStepsFromProfile(
    'profile-Products.ATVocabularyManager:default', ignore_dependencies=True)
    portal_setup.runImportStepFromProfile(PROFILEID, 'skins', run_dependencies=False)
    log.warn('Upgrade v1005 runned.')


def constrain_mars(portal):
    try:
        mars = portal.restrictedTraverse('collections')
    except:
        mars = None
    try:
        collections = portal.restrictedTraverse('collections/collections')
    except:
        collections = None
    try:
        sites = portal.restrictedTraverse('collections/sites')
    except:
        sites = None
    if sites is not None:
        sites.setConstrainTypesMode(1)
        sites.setLocallyAllowedTypes(
            ('Folder', 'Mars Site', 'Topic')
        )
        sites.setImmediatelyAddableTypes(
            ('Folder', 'Mars Site', 'Topic')
        )
    if collections is not None:
        mars.setConstrainTypesMode(1)
        collections.setLocallyAllowedTypes(
            ('Mars Collection', 'Folder')
        )
        collections.setImmediatelyAddableTypes(
            ('Mars Collection', 'Folder')
        )
    if mars is not None:
        mars.setConstrainTypesMode(1)
        mars.setLocallyAllowedTypes(
            ('Collection', 'Folder', 'Topic')
        )
        mars.setImmediatelyAddableTypes(
            ('Collection', 'Folder', 'Topic')
        )

def v1006(portal_setup):
    """
    """
    portal = site = portal_setup.aq_parent
    qi = site.portal_quickinstaller
    pm = portal.portal_migration
    catalog = getToolByName(portal, 'portal_catalog')
    portal_setup.runAllImportStepsFromProfile(
        'profile-Products.ATVocabularyManager:default', ignore_dependencies=True)
    migration_util.loadMigrationProfile(
        site,
        'profile-mars.policy.migrations:1006')
    portal_setup.runAllImportStepsFromProfile(
        'profile-plone.app.collection:default')

    for step in [
        'typeinfo',
        'factorytool',
        'propertiestool',
    ]:
        portal_setup.runImportStepFromProfile(
            PROFILEID, step, run_dependencies=False)
    for step in [
        'marscats',
    ]:
        portal_setup.runImportStepFromProfile(
            TPROFILEID, step, run_dependencies=False)
    oldmap = {
        'Collection': {
            'om': 'Collection', 'op':'Collection',
            'm': 'MarsCollection', 'p':'Mars Collection',
        },
        'Site': {
            'om': 'Site', 'op':'Site',
            'm': 'MarsSite', 'p':'Mars Site',
        },
    }
    constrain_mars(portal)
    brains = catalog.search({'portal_type': oldmap.keys()})
    for item in brains:
        obj = item.getObject()
        info = oldmap[obj.portal_type]
        changed = False
        if obj.portal_type == info['op']:
            obj.portal_type = info ['p']
            changed = True
        if obj.meta_type == info['om']:
            obj.portal_type = info ['m']
            changed = True
        if changed:
            obj.reindexObject()
    log.warn('Upgrade v1006 runned.')


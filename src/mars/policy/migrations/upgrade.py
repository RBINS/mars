
# -*- coding: utf-8 -*-

import os, sys
import pkg_resources

try:
    from Products.CMFPlone.migrations import migration_util
except:
    #plone4
    from plone.app.upgrade import utils as migration_util

from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.image import IATImage
from Products.ATContentTypes.content.image import ATImage
import transaction

from Products.CMFPlone.utils import _createObjectByType

import logging

log = logging.getLogger('mars migrations')
PROFILEIDS = 'mars.policy:z_mars_plone'
PROFILEID = 'profile-%s' % PROFILEIDS
TPROFILEIDS = 'mars.policy:default'
TPROFILEID = 'profile-%s' % PROFILEIDS
root = pkg_resources.resource_filename('mars.policy', '/')

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


def v1007(context):
    purl = getToolByName(context, 'portal_url')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    report = pm.upgrade(dry_run=False)
    for i in catalog.search({'portal_type': 'PDF Folder'}):
        obj = i.getObject()
        parent = obj.aq_parent.aq_inner
        id = obj.getId()
        parent.manage_delObjects([id])
    for i in catalog.search({'portal_type': 'MarsPDFFile'}):
        obj = i.getObject()
        parent = obj.aq_parent.aq_inner
        content = obj.getField('file', obj).get(obj).data.data
        id = obj.getId()
        t = obj.Title()
        d = obj.Description()
        parent.manage_delObjects([id])
        nobj = _createObjectByType('File',
                           parent,
                           id)
        nobj.processForm()
        nobj.setTitle(t)
        nobj.setDescription(d)
        nobj.getField('file', nobj).set(nobj, content)
    tps = ('Mars Collection', 'Folder', 'Topic', 'Collection')
    collections = portal['collections']
    collections.setLocallyAllowedTypes(tps)
    collections.setImmediatelyAddableTypes(tps)
    log.warn('Upgrade v1007 runned.')

def v1008(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    report = pm.upgrade(dry_run=False)
    for step in [
        'typeinfo',
    ]:
        portal_setup.runImportStepFromProfile(
            PROFILEID, step, run_dependencies=False)
    recook_resources(portal_setup)
    log.warn('Upgrade v1008 runned.')
 
def v1009(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    report = pm.upgrade(dry_run=False)
    for step in [
        'mars_policy_logo',
    ]:
        portal_setup.runImportStepFromProfile(
            PROFILEID, step, run_dependencies=False)
    recook_resources(portal_setup)
    log.warn('Upgrade v1009 runned.')
        
def v1010(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    report = pm.upgrade(dry_run=False)
    keyfile = os.path.join(root, 'aviary.txt')
    for step in [
        'atcttool',
    ]:
        portal_setup.runImportStepFromProfile(
            PROFILEID, step, run_dependencies=False)
    portal_setup.runAllImportStepsFromProfile(
    'profile-collective.externalimageeditor:default', ignore_dependencies=True)
    from zope.component import getUtility
    from plone.registry.interfaces import IRegistry
    from collective.externalimageeditor import interfaces as eie
    registry = getUtility(IRegistry)
    settings = registry.forInterface(
            eie.IExternalimageeditorConfiguration) 
    if not os.path.exists(keyfile):
        raise Exception('You must create %s in the form key:keysecret' % keyfile)

    key, secret=open(keyfile).read().strip('\n').split(':')
    settings.has_aviary = True
    settings.has_pixlr = True
    settings.aviary_key = key
    settings.aviary_secret = secret
    recook_resources(portal_setup)
    log.warn('Upgrade v1010 runned.')
        

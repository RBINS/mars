# -*- coding: utf-8 -*-

import os
from StringIO import StringIO

import pkg_resources
from Testing.makerequest import makerequest
from collective.externalimageeditor import interfaces as eie
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

try:
    from Products.CMFPlone.migrations import migration_util
except:
    #plone4
    from plone.app.upgrade import utils as migration_util

from Products.CMFCore.utils import getToolByName
import transaction

from Products.CMFPlone.utils import _createObjectByType
from collective.ckeditor.setuphandlers import (
    registerTransformPolicy,
    DOCUMENT_DEFAULT_OUTPUT_TYPE,
    REQUIRED_TRANSFORM)

import logging

log = logging.getLogger('mars migrations')
PRODUCT = 'mars.policy'
PROFILEIDS = 'mars.policy:z_mars_plone'
PROFILEID = 'profile-%s' % PROFILEIDS
TPROFILEIDS = 'mars.policy:default'
TPROFILEID = 'profile-%s' % PROFILEIDS
root = pkg_resources.resource_filename('mars.policy', '/')


def log(message, level='info'):
    logger = logging.getLogger('%s.upgrades' % PRODUCT)
    getattr(logger, level)(message)


def commit(context):
    transaction.commit()
    context._p_jar.sync()


def quickinstall_addons(context, install=None, uninstall=None, upgrades=None):
    qi = getToolByName(context, 'portal_quickinstaller')

    if install is not None:
        for addon in install:
            if qi.isProductInstallable(addon):
                qi.installProduct(addon)
                log('Installed %s' % addon)
            else:
                log('%s can t be installed' % addon, 'error')

    if uninstall is not None:
        for p in uninstall:
            if qi.isProductInstalled(p):
                qi.uninstallProducts([p])
                log('Uninstalled %s' % p)

    if upgrades is not None:
        if upgrades in ("all", True):
            # find which addons should be upgrades
            installedProducts = qi.listInstalledProducts(showHidden=True)
            upgrades = [p['id'] for p in installedProducts]
        for upgrade in upgrades:
            # do not try to upgrade myself -> recursion
            if upgrade == PRODUCT:
                continue
            try:
                qi.upgradeProduct(upgrade)
                log('Upgraded %s' % upgrade)
            except KeyError:
                log('can t upgrade %s' % upgrade, 'error')


def recook_resources(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    jsregistry = getToolByName(site, 'portal_javascripts')
    cssregistry = getToolByName(site, 'portal_css')
    jsregistry.cookResources()
    cssregistry.cookResources()
    log('Recooked css/js')


def import_js(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(PROFILEID, 'jsregistry', run_dependencies=False)
    log('Imported js')


def import_css(context):
    """
    """
    site = getToolByName(context, 'portal_url').getPortalObject()
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(PROFILEID, 'cssregistry', run_dependencies=False)
    log('Imported css')


def css_upgrade(portal_setup):
    portal = site = portal_setup.aq_parent
    portal_setup.runImportStepFromProfile(PROFILEID, 'cssregistry', run_dependencies=False)
    transaction.commit()
    log('Css upgraded')


def js_upgrade(portal_setup):
    portal = site = portal_setup.aq_parent
    portal_setup.runImportStepFromProfile(PROFILEID, 'jsregistry', run_dependencies=False)
    transaction.commit()
    log('Js upgraded')


def recook_resources(portal_setup):
    portal = site = portal_setup.aq_parent
    jsregistry = getToolByName(site, 'portal_javascripts')
    cssregistry = getToolByName(site, 'portal_css')
    jsregistry.cookResources()
    cssregistry.cookResources()
    transaction.commit()
    log('Recooked resources (js/css)')


def upgrade_profile(context, profile_id, steps=None):
    """
    >>> upgrade_profile(context, 'foo:default')
    """
    portal_setup = getToolByName(context.aq_parent, 'portal_setup')
    gsteps = portal_setup.listUpgrades(profile_id)
    class fakeresponse(object):
        def redirect(self, *a, **kw): pass
    class fakerequest(object):
        RESPONSE = fakeresponse()
        def __init__(self):
            self.form = {}
            self.get = self.form.get
    fr = fakerequest()
    if steps is None:
        steps = []
        for col in gsteps:
            if not isinstance(col, list):
                col = [col]
            for ustep in col:
                steps.append(ustep['id'])
        fr.form.update({
            'profile_id': profile_id,
            'upgrades': steps,
        })
    portal_setup.manage_doUpgrades(fr)


def upgrade_plone(portal_setup):
    """
    """
    out = StringIO()
    portal = makerequest(
        getToolByName(
            portal_setup, 'portal_url'
        ).getPortalObject(),
        stdout=out, environ={'REQUEST_METHOD':'POST'})
    # pm = getToolByName(portal, 'portal_migration')
    # use direct acquisition for REQUEST to be always there
    pm = portal.portal_migration
    report = pm.upgrade(dry_run=False)
    return report


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
    log('Upgrade v1000 runned.')


def v1003(portal_setup):
    """
    """
    portal = site = portal_setup.aq_parent
    qi = site.portal_quickinstaller
    pm = portal.portal_migration
    report = pm.upgrade(dry_run=False)
    transaction.commit()
    log('Upgrade v1003 runned.')


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
    log('Upgrade v1004 runned.')


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
    log('Upgrade v1005 runned.')


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
    log('Upgrade v1006 runned.')


def v1007(context):
    purl = getToolByName(context, 'portal_url')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    report = pm.upgrade(dry_run=False)
    #for i in catalog.search({'portal_type': 'PDF Folder'}):
    #    obj = i.getObject()
    #    parent = obj.aq_parent.aq_inner
    #    id = obj.getId()
    #    parent.manage_delObjects([id])
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
    log('Upgrade v1007 runned.')


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
    log('Upgrade v1008 runned.')


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
    log('Upgrade v1009 runned.')


def configure_eie(context):
    keyfile = os.path.join(root, 'aviary.txt')
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


def v1010(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    for step in [
        'atcttool',
    ]:
        portal_setup.runImportStepFromProfile(
            PROFILEID, step, run_dependencies=False)
    portal_setup.runAllImportStepsFromProfile(
     'profile-collective.externalimageeditor:default', ignore_dependencies=True)
    configure_eie(portal)
    recook_resources(portal_setup)
    log('Upgrade v1010 runned.')


def v1011(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    for step in [
        'skins',
    ]:
        portal_setup.runImportStepFromProfile(
            PROFILEID, step, run_dependencies=False)
    recook_resources(portal_setup)
    log('Upgrade v1011 runned.')


def v1012(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    for item in catalog.search({
        'portal_type': [
            'Analysis',
            'Analysis Absolute Dating',
            'Analysis Relative Dating',
        ]
    }):
        item.getObject().reindexObject()
    recook_resources(portal_setup)
    log('Upgrade v1012 runned.')


def v1013(context):
    purl = getToolByName(context, 'portal_url')
    portal_setup = getToolByName(context, 'portal_setup')
    portal = site = purl.getPortalObject()
    qi = site.portal_quickinstaller
    ttool = getToolByName(context, 'portal_types')
    catalog = getToolByName(portal, 'portal_catalog')
    pm = getToolByName(portal, 'portal_migration')
    #for i in catalog.search({'portal_type': 'PDF Folder'}):
    #    obj = i.getObject()
    #    parent = obj.aq_parent.aq_inner
    #    id = obj.getId()
    #    parent.manage_delObjects([id])
    #    parent.reindexObject()
    recook_resources(portal_setup)
    log('Upgrade v1013 runned.')


def v1014(context):
    upgrade_plone(context)
    log('Upgrade v1014 runned.')


def v1015(context):
    upgrade_plone(context)
    log('Upgrade v1015 runned.')


def v1016(context):
    quickinstall_addons(
        context,
        uninstall=['kupu'],
        upgrades=[
            'collective.ckeditor',
            'CMFPlomino',
            'plone.app.dexterity',
            'plone.app.jquery',
            'collective.quickupload',
            'collective.js.jqueryui',
            'collective.js.datatables',
        ])
    import_js(context)
    import_css(context)
    recook_resources(context)
    # https://dev.plone.org/ticket/13645
    site = getToolByName(context, 'portal_url').getPortalObject()
    registerTransformPolicy(
        site, DOCUMENT_DEFAULT_OUTPUT_TYPE,
        REQUIRED_TRANSFORM)
    log('Upgrade v1016 runned.')


def v1017(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(PROFILEID, 'browserlayer', run_dependencies=True)
    log('Upgrade v1017 runned.')


def v1018(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-Products.PloneKeywordManager:default')
    portal_setup.runAllImportStepsFromProfile('profile-collective.z3cform.widgets:default')
    portal_setup.runImportStepFromProfile(PROFILEID, 'actions', run_dependencies=True)
    log('Upgrade v1018 runned.')


def v1019(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runAllImportStepsFromProfile('profile-plone.app.ldap:ldap')
    log('Upgrade v1019 runned.')


def v1020(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile(PROFILEID, 'rolemap', run_dependencies=True)


def v1021(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'jsregistry', run_dependencies=False)
    recook_resources(context)


def v1022(context):
    portal_setup = getToolByName(context, 'portal_setup')
    portal_setup.runImportStepFromProfile('profile-mars.policy:z_mars_plone', 'viewlets', run_dependencies=False)

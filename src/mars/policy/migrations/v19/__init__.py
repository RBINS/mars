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
    l = logging.getLogger('mars/policy/migrations/v19')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site, 'profile-Products.PloneSurvey:default')
    #migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v19:18-19')
    #portal_setup.runImportStepFromProfile('profile-collective.zipfiletransport:default', 'actions')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    #portal_setup.runAllImportStepsFromProfile('profile-collective.js.datatables:default')
    #portal_setup.runAllImportStepsFromProfile('profile-eea.facetednavigation:default')
    tt = site.portal_types
    indexes =  catalog.indexes()
    request = site.REQUEST
    mars = site['collections']
    for item in tt.objectIds():
        fti = tt.restrictedTraverse(item)
        if 'marsapp.content' in fti.product:
            l.error('-'*80)
            l.error(fti.id) 
            iid = 'formigrationdeleteme'
            try:
                if iid in mars.objectIds():
                    mars.manage_delObjects([id])
                try:
                    id = mars.invokeFactory(fti.content_meta_type, iid)
                except ValueError, e:
                    try:
                        id = mars.invokeFactory(fti.title, iid)
                    except ValueError, e:
                        id = mars.invokeFactory(fti.id, iid)
            except Exception, e:
                import pdb;pdb.set_trace()  ## Breakpoint ##

            inst = mars[id]
            filtered = ['locallyAllowedTypes', 
                        'immediatelyAddableTypes']
            try:
                if inst is not None:
                    for key in inst.schema.keys():
                        field = inst.schema[key]
                        if field.__name__ in filtered:
                            l.error('Skipping filtered: %s' % field.__name__)
                            continue
                        if getattr(field, 'vocabulary', None):
                            notwanted = ['categorization', 'settings']
                            if not field.schemata in notwanted:
                                ik = field.accessor
                                if (isinstance(field, StringField)
                                    or isinstance(field, IntegerField) 
                                   ):
                                    if ik in indexes:
                                        if catalog.Indexes[ik].meta_type != 'KeywordIndex':
                                            l.error('Recreating %s' % ik)
                                            catalog.delIndex(ik)
                                            catalog.addIndex(ik, 'KeywordIndex')
                                            catalog.reindexIndex(ik, request)
                                            transaction.commit()
                                        else:
                                            print "Already done for %s" % ik
            finally:
                mars.manage_delObjects([id])

                


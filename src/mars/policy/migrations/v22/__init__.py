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
    l = logging.getLogger('mars/policy/migrations/v22')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    request = site.REQUEST
    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site, 'profile-Products.PloneSurvey:default')
    #migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v22:21-22')
    #portal_setup.runImportStepFromProfile('profile-collective.zipfiletransport:default', 'actions')
    #portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'catalog', run_dependencies=False)
    portal_setup.runImportStepFromProfile('profile-mars.policy:default', 'atcttool', run_dependencies=False)
    #portal_setup.runAllImportStepsFromProfile('profile-collective.js.datatables:default')
    mtypes = tuple(REFERENCE_SAMPLES) + tuple(DISCOVERY_PLACES) + ("Collection",)
    for item in catalog.searchResults(**{'portal_type': mtypes}):
        def migrate(obj, index, ftype):
            value = obj.getField(index).getAccessor(obj)()
            if ((ftype == 'date' and isinstance(value, int))
                or (ftype=='int' 
                    and isinstance(value, (DateTime, datetime.date)))):
                try:
                    if ftype == 'int':
                        if isinstance(value, datetime.date):
                            dvalue = value.year
                        elif isinstance(value, DateTime):
                            dvalue = value.year()
                        else:
                            dvalue = int(value)
                    if ftype == 'date':
                        dvalue = DateTime(
                        datetime.datetime(int(value), 1, 1))
                except:
                    dvalue = None
                l.error('Migrating %s / %s %s => %s ' % (
                    '/'.join(obj.getPhysicalPath()),
                    i,
                    value,
                    dvalue,
                )) 
                obj.getField(index).getMutator(obj)(dvalue)
                obj.reindexObject()
        obj = item.getObject()
        k = obj.schema.keys()
        indexes = {'date':['endingYear', 'beginningYear', 'year'], 'int': ['BPDating']}
        for kk in indexes:
            for i in indexes[kk]:
                if i in k:
                    migrate(obj, i, ftype=kk)
    #portal_setup.runAllImportStepsFromProfile('profile-plone.formwidget.datetime:default')
    ## reindex new indexes
    #for i in catalog.indexes():
    #    if not i in indexes:
    #        l.error('Reindexing %s' % i)
    #        catalog.reindexIndex(i, request)

    # migrate fields to datetimefields


    #portal_setup.runAllImportStepsFromProfile('profile-eea.facetednavigation:default')
                


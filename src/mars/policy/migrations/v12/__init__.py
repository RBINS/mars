# -*- coding: utf-8 -*-

import os, sys

try:
    from Products.CMFPlone.migrations import migration_util
except:
    #plone4
    from plone.app.upgrade import utils as migration_util

from Products.CMFCore.utils import getToolByName

from marsapp.content.schemata.vocabularies import MarsTypes


def upgrade(portal_setup):
    """
    """
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    brains = catalog.searchResults({
        'portal_type' : MarsTypes,
    })
    objs = [b.getObject() for b in brains]

    for o in objs:
        schema = o.schema
        nfield = 'coordinatesOthers'
        if nfield in schema.keys():
            try:
                value = o.getCoordinatesOthers()
            except:
                value = o.getField(nfield).getStorage().get(nfield, o)
            nval  = '\n'.join(value) 
            if (isinstance(value, list) 
                or isinstance(value, tuple)):
                try:
                    o.setCoordinatesOthers(nval)
                except:
                    o.getField(nfield).getStorage().set(nfield, o, nval)
                o.reindexObject()


    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site,
    #                                    'profile-Products.PloneSurvey:default')

    migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v12:11-12') 





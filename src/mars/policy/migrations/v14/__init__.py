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

def migrate(folder):
    """ migrate existing data structure from a regular folder to a btree
        folder;  the folder needs to be btree-based already """
    folder = aq_base(folder)
    assert isinstance(folder, BTreeFolder)
    assert folder.getId()       # make sure the object is properly loaded
    has = folder.__dict__.has_key
    #if has('_tree') and not has('_objects'):
    #    return False            # already migrated...
    folder._initBTrees()        # create _tree, _count, _mt_index
    for info in folder._objects:
        name = info['id']
        # _setOb will notify the ordering adapter itself,
        # so we don't need to care about storing order information here...
        folder._setOb(name, aq_base(getattr(folder, name)))
        delattr(folder, name)
    if has('_objects'):
        delattr(folder, '_objects')
    folder.reindexObject()
    return True

def upgrade(portal_setup):
    """
    """
    l = logging.getLogger('mars/policy/migrations/v14')
    site = portal_setup.aq_parent
    catalog = site.portal_catalog
    brains = catalog.searchResults({'portal_type': ['Site', 'Excavation', 'Stratigraphy']})
    objs = [o.getObject() for o in brains]
    for o in objs:
        ordering = o.getOrdering()
        order = ordering._order()
        for a in o.objectIds(ordered=False):
            if not a in order:
                l.error(
                    'Adding %s in %s.order' % (
                        a,
                        '/'.join(o.getPhysicalPath()),
                    )
                )
                o.getOrdering().notifyAdded(a)


    # install Products.PloneSurvey and dependencies
    #migration_util.loadMigrationProfile(site,
    #                                    'profile-Products.PloneSurvey:default')

    migration_util.loadMigrationProfile( site, 'profile-mars.policy.migrations.v14:13-14')



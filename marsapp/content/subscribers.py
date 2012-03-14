#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'
from Products.Archetypes.event import ObjectInitializedEvent 
from Products.CMFCore.utils import getToolByName
import logging
from zope.event import notify
def create_files_and_images_folders(obj, event):
    log = logging.getLogger('create_files_and_images_folders')
    wf_tool = getToolByName(obj, 'portal_workflow')
    folders = {'images':'Images',
               'files': 'Files',}
    try:
        for folder in folders:
            if not folder in obj.objectIds():
                nt = obj.invokeFactory('Folder', folder)
                subf = obj[nt]
                subf.setTitle(folders[folder])
                subf.unmarkCreationFlag()
                subf.reindexObject()
                notify(ObjectInitializedEvent(subf)) 
                rs = wf_tool.getInfoFor(subf, 'review_state', '')
                if folder == 'images':
                    subf.setLayout("atct_album_view")

                if not rs == 'published':
                    wf_tool.doActionFor(
                        subf,
                        "publish",
                        comment="publised programmatically")
    except Exception, e:
        msg = 'Ooops, %s' % e
        log.error(msg)

# vim:set et sts=4 ts=4 tw=80:

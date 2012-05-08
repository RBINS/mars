#-*- coding: utf-8 -*-
"""
MARS csvreplicata handlers installation.
"""

from Products.CMFCore.utils import getToolByName

def importVarious(context):
    #installs mars handlers for csvreplicata
    site = context.getSite()
    csvtool = getToolByName(site, 'portal_csvreplicatatool')
                       


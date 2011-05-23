"""
MARS csvreplicata handlers installation.
"""
from Products.CMFCore.utils import getToolByName
from utils import CSVMarsCat, CSVMarsCoordinates

def importVarious(context):
    #installs mars handlers for csvreplicata
    site = context.getSite()
    csvtool = getToolByName(site, 'portal_csvreplicatatool')
    csvtool.setHandler('marsapp.categories.field.MarscatField',
                       {'handler_class': CSVMarsCat(), 'file': False})
    csvtool.setHandler('marsapp.content.schemata.field.CoordinatesField',
                       {'handler_class': CSVMarsCoordinates(), 'file': False})
    return

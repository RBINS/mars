#-*- coding: utf-8 -*-

from Products.csvreplicata import AppConfig
from Products.CMFCore.utils import getToolByName
import logging
from utils import CSVMarsCat, CSVMarsCoordinates 

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    logging.getLogger('mars csreplicata').warn('registering mars plugins')
    AppConfig.HANDLERS.update({
        'marsapp.categories.field.MarscatField': {
            'handler_class': CSVMarsCat(), 
            'file': False},
        #'marsapp.categories.field.MarscatField':  {
        #    'handler_class' : reference.CSVReference(), 
        #    'file' : False},
        'marsapp.content.schemata.field.CoordinatesField': {
            'handler_class': CSVMarsCoordinates(), 
            'file': False},
    })

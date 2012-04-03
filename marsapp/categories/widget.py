#-*- coding: utf-8 -*-
#from Acquisition import aq_base, aq_inner, aq_parent
from zope.component import getMultiAdapter
#from Products.Five.browser import BrowserView
#from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.Registry import registerWidget

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

class ReferenceBrowserWidget(ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update({
        'macro': 'marsrefbrowser',
        'image_portal_types':['Image',],
        'image_method':'image_thumb', 
    })

class MarscatWidget(ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update({
        'macro': 'marscats4browser',
        'popup_name' : 'mars_popup',
        'restrict_browsing_to_startup_directory': True,
        })

registerWidget(MarscatWidget,
    title='Mars Categories Browser',
    description=('Reference widget that allows you to browse or'
                 'search the portal for categories to refer to.'),
    used_for=('Products.marscats.Field.MarscatField',)
    )


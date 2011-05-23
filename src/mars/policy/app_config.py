#-*- coding: utf-8 -*-
"""Specific project configuration."""
GLOBALS = globals()




################################################################################
# Products that have entries in quickinstaller,
# here are their 'id' (not the translated name)
################################################################################

PRODUCT_DEPENDENCIES = (\
)

EXTENSION_PROFILES = ('mars.policy:default',)

SKIN = 'mars.skin'
HIDDEN_PRODUCTS = [u'plone.app.openid', u'NuPlone',
#      u'plone.app.blob',
#      u'plone.app.dexterity',
#      u'Products.TinyMCE',
#      u'Products.ContentWellPortlets',
#      u'Products.csvreplicata',
#      u'plone.app.z3cform',
    #with_ploneproduct_dexterity

#    u'plone.app.dexterity',
    #with_ploneproduct_contentwellportlet

#    u'ContentWellPortlets',
    #with_ploneproduct_csvreplica
         #'csvreplicata',
#        #with_ploneproduct_tinymce

#    u'TinyMCE',
#    u'mars.skin',
#    u'mars.tma',
#    u'mars.policy.migrations.v1_1',
#    u'mars.policy.migrations',
#    u'csvreplicata',
#    u'Products.csvreplicata',
]
HIDDEN_PROFILES = [u'plone.app.openid', u'NuPlone',
    u'mars.skin',
    u'mars.tma',
    u'mars.policy.migrations.v1_1',
    u'mars.policy.migrations',
      u'plone.app.blob',
      u'plone.app.dexterity',
      u'Products.TinyMCE',
      u'Products.ContentWellPortlets',
      u'Products.csvreplicata',
      u'plone.app.z3cform',
#    u'csvreplicata',
#    u'Products.csvreplicata',

]

from zope.interface import implements
from Products.CMFQuickInstallerTool.interfaces import INonInstallable as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable as INonInstallableProfiles

class HiddenProducts(object):
    implements(INonInstallableProducts)

    def getNonInstallableProducts(self):
        return HIDDEN_PRODUCTS

class HiddenProfiles(object):
    implements(INonInstallableProfiles)

    def getNonInstallableProfiles(self):
        return [ u'plone.app.openid', u'NuPlone', ]

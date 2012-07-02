#-*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8
"""
__init__.py

Created by David Convent on 2008-06-25.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

import unittest, doctest

from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
ztc.installProduct('CMFBibliographyAT')
ztc.installProduct('ATBiblioList')
ztc.installProduct('ATBiblioStyles')
ztc.installProduct('ATBiblioTopic')
ztc.installProduct('AmazonTool')
ztc.installProduct('PubmedClient')
ztc.installProduct('marsapp.categories')

ptc.setupPloneSite(extension_profiles=('marsapp.policy:default',))


def test_suite():
    return unittest.TestSuite((
    
        ztc.ZopeDocFileSuite(
            'README.txt', package='marsapp.helpers',
            test_class=ptc.FunctionalTestCase,
            optionflags=(doctest.ELLIPSIS | 
                         doctest.NORMALIZE_WHITESPACE)),
    ))

if __name__ == "__main__":
    unittest.main(defaultTest='test_suite')

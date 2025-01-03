# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='mars',
      version=version,
      description="",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.rst")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='plone mars migration zope archaeology',
      author='Makina Corpus',
      author_email='contact@makina-corpus.com',
      url='http://www.naturalsciences.be',
      license='GPL',
      namespace_packages=['mars', 'marsapp'],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'bibliograph.core',
          'bibliograph.parsing',
          'bibliograph.rendering',
          'collective.bibliocustomviews',
          'rbins_masschange',
          'rbins.restapi',
          'rbins.csvimport',
          'collective.actions.delete',
          'collective.ckeditor',
          'collective.excelexport',
          'collective.externalimageeditor',
          'collective.geo.bundle',
          'collective.pfg.dexterity',
          'collective.js.jqueryui',
          'collective.js.datatables',
          'collective.quickupload',
          'collective.taxonomy',
          'collective.testcaselayer',
          'collective.tablepage',
          'collective.uploadify',
          'collective.zipfiletransport',
          'demjson',
          'ecreall.helpers.upgrade',
          'eea.facetednavigation',
          'five.grok',
          'ordereddict',
          'PasteScript',
          'Plomino',
          'plomino.tinymce',
          'Plone',
          'plone.app.dexterity [grok,relations]',
          'plone.restapi',
          'collective.z3cform.keywordwidget',
          'plone.app.testing',
          'plone.directives.form',
          'plone.formwidget.datetime',
          'Products.ATVocabularyManager',
          'Products.PloneKeywordManager',
          'Products.CMFBibliographyAT',
          'Products.contentmigration',
          'Products.ContentWellPortlets',
          'Products.csvreplicata',
          'Products.PloneKeywordManager',
          'collective.z3cform.widgets',
          'Products.Maps',
          'collective.dexteritytextindexer',
          'collective.googleanalytics',
          'Products.RefBiblioParser',
          'Products.RefBiblioParser',
          'Products.TinyMCE',
          'setuptools',
          'z3c.autoinclude',
          'chardet',
          'z3c.blobfile',
          'z3c.form[test]',
          'zc.buildout',
          'lxml',
          'zope.component',
          'zope.interface',
          'z3c.jbot',
          'zope.testing',
          'six',
          'collective.importexport',
          'collective.exportimport',
      ],
      entry_points={
          'z3c.autoinclude.plugin': [
              'target = plone',
          ],
      },
      extras_require={'ldap': ['plone.app.ldap'],
                      'test': ['IPython', 'zope.testing', 'mocker']},
      )

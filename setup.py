from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='marsapp.helpers',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
          "Framework :: Zope2",
          "Framework :: Zope3", 
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone mars migration zope archaeology',
      author='Mathieu Le Marec - Pasquet',
      author_email='kiorky@cryptelium.net',
      url='http://naturalsciences.be',
      license='GPL',
      namespace_packages=[                'mars', 'mars.testing', 'marsapp'],  
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'collective.testcaselayer',
          'demjson',
          #'plone.reload',
          'ordereddict',
          'Products.CMFBibliographyAT',
          'Products.contentmigration',
          'Products.csvreplicata',
          'setuptools',
          'z3c.autoinclude',
          'zope.component',
          'zope.interface',
          'zope.testing',
      ],
      entry_points = {
          'z3c.autoinclude.plugin': [
              'target = plone',
          ], 

      }, 

      extras_require={'test': ['IPython', 'zope.testing', 'mocker']},
     )

#-*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.1'


setup(name='marsapp.policy',
      version=version,
      description="Policy package for setting up a MARS portal",
      long_description="""\
      """,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Zope2",
          "Framework :: Zope3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='zope plone archaeology',
      author='David Convent',
      author_email='mars@naturalsciences.be',
      url='http://www.naturalsciences.be/metamars',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=[                'mars', 'mars.testing', 'marsapp'],  
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'collective.testcaselayer',
          'demjson',
          #'plone.reload',
          'Products.CMFBibliographyAT',
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

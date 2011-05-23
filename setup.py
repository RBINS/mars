from setuptools import setup, find_packages
import os

setup(name='marsapp.migration',
      version=version,
      description="Package for migrating old mars items to the new system",
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
      keywords='plone mars migration zope  archaeology',
      author='David Convent',
      author_email='david.convent@naturalsciences.be',
      url='http://svn.naturalsciences.be/projects/mars',
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

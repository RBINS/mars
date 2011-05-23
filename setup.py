import os, sys

from setuptools import setup, find_packages

version = u'1.0'

def read(*rnames):
    return open(
        os.path.join('.', *rnames)
    ).read()

long_description = "\n\n".join(
    [read('README.txt'),
     read('docs', 'INSTALL.txt'),
     read('docs', 'HISTORY.txt'),
    ]
)

classifiers = [
    "Programming Language :: Python",
    "Topic :: Software Development",]


setup(
    name=name,
    namespace_packages=[                'mars', 'mars.testing',],  
    version=version,
    description='Project cadredeville testing product',
    long_description=long_description,
    classifiers=classifiers,
    keywords='',
    author='mpa <mpa@makina-corpus.com>',
    author_email='mpa@makina-corpus.com',
    url='http://pypi.python.org/pypi/%s' % name,
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    install_requires=[
        # -*- Extra requirements: -*-
        'collective.testcaselayer',
        'demjson',
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
# vim:set ft=python:

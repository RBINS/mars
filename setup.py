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

name = 'mars.policy'
setup(
    name=name,
    namespace_packages=[         'mars', 
         'mars.policy',], 
    version=version,
    description='Project cadredeville policy product',
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
        'setuptools',
        'z3c.autoinclude',
        # -*- Extra requirements: -*-
        'collective.testcaselayer',
    ],
    entry_points = {
        'z3c.autoinclude.plugin': [
            'target = plone',
        ], 

    },
)
# vim:set ft=python:

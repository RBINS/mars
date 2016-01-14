
'''configure untrusted python from csv exports'''
import re
import sys
import csv
from AccessControl import allow_type
from AccessControl import ModuleSecurityInfo
from AccessControl import allow_class
from Products.PythonScripts.Utility import allow_module


for i in [
    'csv',
    'datetime',
    're',
    'time',
    'urllib',
    'urllib2',
    'StringIO',
    'cStringIO',
    'rbins_masschange',
    'rbins_masschange.utils',
]:
    exec 'import {0}'.format(i)
    allow_module(i)

allow_class(csv.DictReader)
allow_class(csv.DictWriter)
allow_class(csv.Dialect)
allow_class(csv.excel)
allow_class(csv.excel_tab)
allow_class(csv.Sniffer)


allow_module('re')
ModuleSecurityInfo('re').declarePublic(
    'compile', 'findall', 'match', 'search', 'split', 'sub', 'subn', 'error',
    'I', 'L', 'M', 'S', 'X')
allow_type(type(re.compile('')))
allow_type(type(re.match('x', 'x')))


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

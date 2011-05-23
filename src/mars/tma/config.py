# -*- coding: utf-8 -*-
"""Specific stuff for package."""

import os
import ConfigParser


GLOBALS = globals()
PROJECTNAME = 'mars.tma'

TMA_FOLDER = 'mars_tma_scripts'

# for test without zope machinery
#cfg_name = os.path.abspath("csv_imports.cfg")
cfg_name = "csv_imports.cfg"

# for test without zope machinery
#DEFAULT_CONFIG_FILE = cfg_name
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), cfg_name)

def getImportOptionsFromIni(cfg=DEFAULT_CONFIG_FILE):
    """Get options for testing.
    
    >>> import pprint
    >>> options = getImportOptionsFromIni()
    >>> pprint.pprint(options)
    ({'Folder': ['default',
                 ' categorization',
                 ' dates',
                 ' ownership',
                 ' settings'],
      'News Item': ['default']},
     'publish')
    """
    Config = ConfigParser.ConfigParser()
    Config.read(cfg)
    options = Config.items('csvreplicata-settings', raw=True)
    settings = {}
    for option in options:
        settings[option[0].title()] = option[1].split(',')
    transition = Config.get('csv-wkf-transiton', 'transition')
    
    return settings, transition

if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)

from eea.facetednavigation.browser.app import query
from zope.interface import Interface

try:
    from Products.ATExtensions.datatype import formattablename

    HAS_ATEXTENSIONS = True
except ImportError:
    HAS_ATEXTENSIONS = False

if HAS_ATEXTENSIONS:
    if not hasattr(formattablename, '_old_abbreviate'):

        formattablename._old_abbreviate = formattablename.abbreviate


        def two_bytes_chars_capable_abbreviate(value, *args, **kwargs):
            if type(value) == str:
                value = unicode(value, encoding='utf-8')
                abbrev = formattablename._old_abbreviate(value, *args, **kwargs)
                return abbrev.encode('utf-8')
            else:
                return formattablename._old_abbreviate(value, *args, **kwargs)


        formattablename.abbreviate = two_bytes_chars_capable_abbreviate

query.DEFAULT_NUM_PER_PAGE = 10000

from collective.excelexport.exportables.dexterityfields import TextFieldRenderer as DxTextFieldRenderer
from collective.excelexport.exportables.archetypesfields import TextFieldRenderer as AtTextFieldRenderer

AtTextFieldRenderer.truncate_at = 2048
DxTextFieldRenderer.truncate_at = 2048

try:
    import Products.PDBDebugMode.pdblogging
    import re

    Products.PDBDebugMode.pdblogging._mars_old_matchers = Products.PDBDebugMode.pdblogging.ignore_matchers
    Products.PDBDebugMode.pdblogging.ignore_matchers = Products.PDBDebugMode.pdblogging._mars_old_matchers + (
        re.compile(r".*Couldn't load state for.*").search,
        re.compile(r".*No blob file.*").search,
    )
except ImportError:
    print("Products.PDBDebugMode.pdblogging not available")
    pass


# https://redmine.makina-corpus.net/issues/19156
# https://stackoverflow.com/questions/5122465/can-i-fake-a-package-or-at-least-a-module-in-python-for-testing-purposes

def new_module(name, doc=None):
    import sys
    from types import ModuleType
    m = ModuleType(name, doc)
    m.__file__ = name + '.py'
    sys.modules[name] = m
    return m


fakebbb = new_module("plone.app.folder.bbb", "fake bbb module")


class IArchivable(Interface):
    pass


class IPhotoAlbumAble(Interface):
    pass


fakebbb.IArchivable = IArchivable
fakebbb.IPhotoAlbumAble = IPhotoAlbumAble

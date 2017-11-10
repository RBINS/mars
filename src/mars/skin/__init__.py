import Products.CMFBibliographyAT.content as CMFBibliographyATContent
from Products.ATExtensions.datatype.formattablenames import FormattableNames
from Products.CMFBibliographyAT.content.base import BaseEntry
# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

modules = [getattr(CMFBibliographyATContent, c) for c in dir(CMFBibliographyATContent) if not c.startswith('__')]
for module in modules:
    # get all bibliography content classes
    klass = [getattr(module, k) for k in dir(module) if k.endswith('Reference')]
    klass = [k for k in klass if BaseEntry in k.__bases__]
    if klass:
        klass = klass[0]
    else:
        continue

    klass.schema.get('subject').widget.helper_js = ('keywordmultiselect.js',)
    klass.schema.get('keywords').widget.helper_js = ('keywordmultiselect.js',)

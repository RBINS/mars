from eea.facetednavigation.browser.app import query

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

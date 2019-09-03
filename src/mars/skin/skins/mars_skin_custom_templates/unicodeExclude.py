## Script (Python) "unicodeIntersect"
##title=Test if a unicode string is in a unicode list
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=values, vocab

if vocab is None or len(vocab) == 0:
    return []

def unicodeEncode(value, site_charset=None):
    # Recursively deal with sequences
    tuplevalue = same_type(value, ())
    if (tuplevalue or same_type(value, [])):
        encoded = [unicodeEncode(v) for v in value]
        if tuplevalue:
            encoded = tuple(encoded)
        return encoded

    if not isinstance(value, basestring):
        value = str(value)

    if site_charset is None:
        site_charset = context.getCharset()

    if same_type(value, ''):
        value = unicode(value, site_charset)

    # don't try to catch unicode error here
    # if one occurs, that means the site charset must be changed !
    return value.encode(site_charset)

unicode_vocab = {unicodeEncode(v) for v in vocab}
unicode_values = [unicodeEncode(v) for v in values]
return [v for v in unicode_values if v not in unicode_vocab]

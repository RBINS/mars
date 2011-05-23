#-*- coding: utf-8 -*-
"""
XML tools to read profile's files.
"""
from xml.dom import minidom

def getProperties(node):
    """Return properties from a node element.
    
    >>> from pprint import pprint
    >>> domobject = minidom.parse('xml_doctests/read_properties.xml')
    >>> node = domobject.documentElement
    >>> properties = getProperties(node)
    >>> pprint(properties)
    {u'count': 12,
     u'default_page': "A property with 'string' attribute",
     u'description': 'A property without type="string"',
     u'empty': '',
     u'enable_permalink': False,
     u'float': 0.0,
     u'selectable_views': (u'folder_listing', u'news_listing'),
     u'validate_email': True}

    """
    props = {}
    for property in node.getElementsByTagName('property'):
        attrs = property.attributes
        name = attrs['name'].nodeValue
        value = ''
        if 'type' in attrs.keys():
            if attrs['type'].nodeValue == 'boolean':
                value = eval(property.childNodes[0].nodeValue)
            if attrs['type'].nodeValue == 'integer':
                value = int(property.childNodes[0].nodeValue)
            if attrs['type'].nodeValue == 'float':
                value = float(property.childNodes[0].nodeValue)
            if attrs['type'].nodeValue == 'string':
                if property.childNodes:
                    value = property.childNodes[0].nodeValue.encode('utf-8')
                else:
                    value = ''
            if attrs['type'].nodeValue == 'lines':
                if property.childNodes:
                    elements = property.getElementsByTagName('element')
                    value = []
                    for element in elements:
                        value.append(element.attributes['value'].nodeValue)
                    value=tuple(value) #lines ar unapcked as tuple in tests
        else :
            if property.childNodes:
                value = property.childNodes[0].nodeValue.encode('utf-8')

        props[name] = value

    return props

if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)
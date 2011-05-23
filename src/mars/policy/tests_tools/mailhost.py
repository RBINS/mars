#-*- coding: utf-8 -*-
"""
Providing MailHost settings from profile to generics tests.
"""
import os.path
from xml.dom import minidom


def getMailHost(xml_file=None):
    """Get MailHost Settings from Profile.

    >>> mailhost_file = 'xml_doctests/mailhost_test.xml'
    >>> mailhost_settings = getMailHost(xml_file=mailhost_file)
    >>> for prop, value in mailhost_settings.iteritems():
    ...     print '%s : %r' %(prop, value)
    smtp_pwd : 'secret'
    smtp_port : 25
    smtp_host : u'smtp.makina-corpus.com'
    smtp_uid : 'user'

    Actually only this four properties are embeded in import/export MailHost
    See Products/GenericSetup/MailHost/exportimport.py
    """
    mailhost = {}
    mh_file = None
    try :
        if not xml_file:
            xml_file = os.path.join(os.path.dirname(__file__), 'xml_doctests', 'mailhost_test.xml')
        mh_file = open(xml_file)
        mh_object = minidom.parse(mh_file)
    except Exception, e:
        print "something wrong loading mailhost xml file"
    if mh_file: mh_file.close()

    mailhost_settings = mh_object.getElementsByTagName('object')
    for setting in mailhost_settings:
        attrs = setting.attributes
        #see comment in __doc__
        #if 'name' in attrs.keys():
        #    mailhost['name'] = attrs['name'].nodeValue
        #if 'meta_type' in attrs.keys():
        #    mailhost['meta_type'] = attrs['meta_type'].nodeValue
        if 'smtp_host' in attrs.keys():
            mailhost['smtp_host'] = attrs['smtp_host'].nodeValue
        if 'smtp_port' in attrs.keys():
            mailhost['smtp_port'] = int(attrs['smtp_port'].nodeValue)
        if 'smtp_pwd' in attrs.keys():
            mailhost['smtp_pwd'] = attrs['smtp_pwd'].nodeValue.encode('utf-8')
        if 'smtp_uid' in attrs.keys():
            mailhost['smtp_uid'] = attrs['smtp_uid'].nodeValue.encode('utf-8')

    return mailhost

if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)

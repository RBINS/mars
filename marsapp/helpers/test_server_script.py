#-*- coding: utf-8 -*-
#!/usr/bin/env python
# encoding: utf-8
"""
content_inspector.py

Created by David Convent on 2008-06-25.
Copyright (c) 2008 __MyCompanyName__. All rights reserved.
"""

from subprocess import Popen, PIPE
from StringIO import StringIO

import sys, os

from zope.interface import Interface
#from zope.interface import Attribute
from zope.interface import implements
from zope.component import adapts

from Products.CMFPlone.interfaces import IPloneSiteRoot

class IStuffTester(Interface):
    """
    """

class StuffTester(object):
    """
    """
    implements(IStuffTester)
    adapts(IPloneSiteRoot)

#    def __init__(self, context):
#        self.context = context

    def __call__(self):
        out = StringIO()
        p = Popen('test_stuff.sh', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=False)
        (fi, fo, fe) = (p.stdin, p.stdout, p.stderr)
        fi.write('hum')
        fi.close()
        result = fo.read()
        fo.close()
        error = fe.read()
        fe.close()
        print >> out, 'test_stuff.sh output:'
        if error:
            print >> out, 'Ouch! No test_stuff.sh found in PATH'
        else:
            print >> out, result
        print >> out, '-----\n'
        print >> out, 'sys.path:'
        for path in sys.path:
            print >> out, path
        print >> out, '-----\n'
        print >> out, 'os.environ:'
        print >> out, str(os.environ['PATH'])
        return out.getvalue()


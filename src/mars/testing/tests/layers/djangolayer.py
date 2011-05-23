#!/usr/bin/env python
# -*- coding: utf-8 -*-

__docformat__ = 'restructuredtext en'

import os

dsm = 'mars.testing.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = dsm
from django.test import TestCase
from django.test.client import Client

from django.db import connection
from django.conf import settings
from django.core.management import call_command


db_name = settings.DATABASE_NAME
class DTestCase(TestCase):
    """Override things there if you need"""

    def __init__(self, *args, **kwargs):
        self.dsm = kwargs.get('dsm', dsm)

    def runTest():pass


    def setUp(self):
        """
        Wrapper around default __call__ method to perform common Django test
        set up. This means that user-defined Test Cases aren't required to
        include a call to super().setUp().
        """
        self.client = Client()
        call_command('flush', verbosity=2, interactive=False)
        self._pre_setup()

    def tearDown(self):
        self._post_teardown()

class djangoLayer(object):
    test = None
    dsm = dsm

    @classmethod
    def setUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.dsm
        connection.creation.create_test_db(2, autoclobber=True)
        self.test = DTestCase()

    @classmethod
    def tearDown(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.dsm
        connection.creation.destroy_test_db(db_name, 2) 
    
    @classmethod
    def testTearDown(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.dsm
        self.test.tearDown()

    @classmethod
    def testSetUp(self):
        os.environ['DJANGO_SETTINGS_MODULE'] = self.dsm
        self.test.setUp()

# vim:set et sts=4 ts=4 tw=80:

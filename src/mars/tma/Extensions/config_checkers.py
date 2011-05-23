# -*- coding: utf-8 -*-
"""
Portal Configuration Checkers
"""
__author__ = "Jean-Philippe Camguilhem <jpc@makina-corpus.com>"

from mars.policy.tests.portal_properties import check_portal_properties
from mars.policy.tests.portal_mailhost import check_portal_mailhost

def report(self, test_suite, title_elt):
    """Base report."""

    template = "<h3>Test %s %s report</h3>%s"
    details = ''
    portal = self.portal_url.getPortalObject()

    errors, failures = test_suite(portal)
    if errors:
        details += '<h4>%s error(s) ! :</h4>' % len(errors)
        for error in errors:
            details += '<p>%s</p>' % error[1].split('\n')[-4:-2]
    if failures:
        details += '<h4>%s failure(s) ! :</h4>' % len(failures)
        for failure in failures:
            details += '<p>%s</p>' % failure[1].split('\n')[-2]

    if not failures and not errors:
        details += '<p>All tests run succesfully !</p>'

    return template % (portal.id, title_elt, details)

# functions below will be loaded as externals_methods by QI.install process
# plz give them a name staring with test
# give them a oneliner docstring which will be their title in inde_html page

def test_portal_properties_from_profile(self):
    """Portal properties checker."""

    return report(self, check_portal_properties, 'properties')

def test_portal_mailhost_from_profile(self):
    """Portal mailhost checker."""

    return report(self, check_portal_mailhost, 'mailhost')

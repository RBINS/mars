"""
Programmatically import structure/contents and user/groups to plone.
"""
__author__ = "Jean-Philippe Camguilhem <jpc@makina-corpus.com>"

from Products.CMFPlone import PloneMessageFactory as _
from Products.Archetypes.utils import addStatusMessage
from mars.policy.tests_tools.users_and_groups import getUsersandGroups

def structure_from_csv(self):
    """Import structure/content via csvrepliacta."""

    csvfile = self.REQUEST.form['csv_structure']
    if not csvfile:
        return 'Please provide a csv structure file !'
    else:
        import transaction
        import os
        from zope.interface import alsoProvides, noLongerProvides
        from Products.csvreplicata.interfaces import ICSVReplicable, \
                                                     Icsvreplicata
        from mars.tma.config import getImportOptionsFromIni
        import_settings, default_transition = getImportOptionsFromIni()
        import foo

        # are we in zopetestcase ?
        # if not we have to install temorarly csvreplicata just to import
        # structure else it's installed via base_setup
        zopetestcase = (('ZOPE_TESTCASE' in os.environ)
                    or ('ZOPETESTCASE' in os.environ))

        portal_quickinstaller = self.portal_quickinstaller
        has_csvreplicata = portal_quickinstaller.\
                           isProductInstalled('csvreplicata')

        if not zopetestcase and not has_csvreplicata:
            #install temporarly csvreplicata if not used by policy.
            portal_quickinstaller.installProduct('csvreplicata')
            transaction.savepoint()

        #provide ICSVReplicable to plonesite
        alsoProvides(self, ICSVReplicable)

        csvreplicatatool = self.portal_csvreplicatatool
        # save existents user settings
        if has_csvreplicata:
            old_replicabletypes_settings = csvreplicatatool.replicabletypes

        # register Structure replicabletypes
        csvreplicatatool.replicabletypes = import_settings
        # now import
        replicator = Icsvreplicata(self)
        replicator.csvimport(csvfile, datetimeformat='%d/%m/%Y',
                             wf_transition=default_transition)

        # restore replicabletypes user settings
        if has_csvreplicata :
            csvreplicatatool.replicabletypes = old_replicabletypes_settings

        #remove ICSVReplicable interface for self
        noLongerProvides(self, ICSVReplicable)

        #uninistall csvreplicata if not used by policy
        if not zopetestcase and not has_csvreplicata:
            portal_quickinstaller.uninstallProducts(['csvreplicata'])

        status_message = _(u'structure succesfully imported',
                               default=u'structure succesfully imported')
        addStatusMessage(self.REQUEST, status_message)
        # and redirect him to the fine location
        next_url = self.portal_url()
        self.REQUEST.RESPONSE.redirect(next_url)
        return self.REQUEST.RESPONSE



# users and group

def addMember(self, member):
    """."""
    self.portal_membership.addMember(member['id'], member['id'],
                                     member['roles'],[])

    memb = self.portal_membership.getMemberById(member['id'])
    memb.setMemberProperties(member)


def addGroup(self, group):
    """."""
    self.portal_groups.addGroup(group['name'], group['role'])
    for member in group['members']:
        self.portal_groups.addPrincipalToGroup(member, group['name'])

    gr = self.portal_groups.getGroupById(group['name'])
    gr.setProperties(group)

def setUpMembers(self, members):
    """."""
    for member in members:
        addMember(self, member)

def setUpGroups(self, groups):
    """."""
    for group in groups:
        addGroup(self, group)

def users_from_csv(self):
    """Import users/groups from csv."""
    csvfile = self.REQUEST.form['csv_users']
    if not csvfile:
        return 'Please provide a csv structure file !'
    else:
        members, groups, errors = getUsersandGroups(csvfile)
        if errors:
            status_message = _(u'You have erors in your csvfile !',
                               default=u'You have erors in your csvfile !')
        else:
            setUpMembers(self, members)
            setUpGroups(self, groups)
            status_message = _(u'Users and groups succesfully imported',
                               default=u'Users and groups succesfully imported')
        addStatusMessage(self.REQUEST, status_message)
        # and redirect him to the fine location
        next_url = self.portal_url()
        self.REQUEST.RESPONSE.redirect(next_url)
        return self.REQUEST.RESPONSE


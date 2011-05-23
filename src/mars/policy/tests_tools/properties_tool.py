#-*- coding: utf-8 -*-
"""
Providing propertiestool from profile to generics tests.
"""

import os.path
from xml.dom import minidom
from read_xml_properties import getProperties


def getSiteToolProperties(xml_file=None):
    """Get properties from Profile.

    >>> from pprint import pprint

    >>> site_prop_file = 'xml_doctests/propertiestool.xml'
    >>> propertiestool = getSiteToolProperties(xml_file=site_prop_file)

    >>> pprint(propertiestool[0])
    {u'bottomLevel': '',
     u'currentFolderOnlyInNavtree': False,
     u'enable_wf_state_filtering': False,
     u'idsNotToList': '',
     u'includeTop': True,
     u'metaTypesNotToList': (u'ATBooleanCriterion',
                             u'ATDateCriteria',
                             u'ATDateRangeCriterion',
                             u'ATListCriterion',
                             u'ATPortalTypeCriterion',
                             u'ATReferenceCriterion',
                             u'ATSelectionCriterion',
                             u'ATSimpleIntCriterion',
                             u'ATSimpleStringCriterion',
                             u'ATSortCriterion',
                             u'ChangeSet',
                             u'Discussion Item',
                             u'Plone Site',
                             u'TempFolder',
                             u'ATCurrentAuthorCriterion',
                             u'ATPathCriterion',
                             u'ATRelativePathCriterion'),
     u'name': '',
     u'parentMetaTypesNotToQuery': (u'TempFolder', u'Large Plone Folder'),
     u'root': '/',
     u'showAllParents': True,
     u'sitemapDepth': '',
     u'sortAttribute': 'getObjPositionInParent',
     u'sortOrder': 'asc',
     u'title': 'NavigationTree properties',
     u'topLevel': '',
     u'wf_states_to_show': ''}

    >>> pprint(propertiestool[1])
    {u'allowAnonymousViewAbout': False,
     u'allowRolesToAddKeywords': (u'Manager', u'Reviewer'),
     u'auth_cookie_length': '',
     u'available_editors': (u'None', u'Kupu'),
     u'calendar_future_years_available': '',
     u'calendar_starting_year': '',
     u'default_charset': 'utf-8',
     u'default_contenttype': 'text/html',
     u'default_language': 'en',
     u'default_page': (u'index_html', u'index.html', u'index.htm', u'FrontPage'),
     u'default_page_types': (u'Topic',),
     u'disable_folder_sections': False,
     u'disable_nonfolderish_sections': False,
     u'ellipsis': '...',
     u'enable_inline_editing': False,
     u'enable_link_integrity_checks': True,
     u'enable_livesearch': True,
     u'enable_sitemap': False,
     u'exposeDCMetaTags': False,
     u'ext_editor': False,
     u'external_links_open_new_window': 'false',
     u'forbidden_contenttypes': (u'text/structured',
                                 u'text/restructured',
                                 u'text/x-rst',
                                 u'text/plain',
                                 u'text/plain-pre',
                                 u'text/x-python',
                                 u'text/x-web-markdown',
                                 u'text/x-web-intelligent',
                                 u'text/x-web-textile',
                                 u'text/x-html-captioned'),
     u'icon_visibility': 'enabled',
     u'invalid_ids': (u'actions',),
     u'localLongTimeFormat': '%b %d, %Y %I:%M %p',
     u'localTimeFormat': '%b %d, %Y',
     u'localTimeOnlyFormat': '%I:%M %p',
     u'lock_on_ttw_edit': True,
     u'many_groups': False,
     u'many_users': False,
     u'mark_special_links': 'false',
     u'number_of_days_to_keep': '',
     u'redirect_links': True,
     u'search_results_description_length': '',
     u'title': 'Site wide properties',
     u'typesLinkToFolderContentsInFC': (u'Large Plone Folder', u'Folder'),
     u'typesUseViewActionInListings': (u'Image', u'File'),
     u'types_not_searched': (u'ATBooleanCriterion',
                             u'ATDateCriteria',
                             u'ATDateRangeCriterion',
                             u'ATListCriterion',
                             u'ATPortalTypeCriterion',
                             u'ATReferenceCriterion',
                             u'ATSelectionCriterion',
                             u'ATSimpleIntCriterion',
                             u'ATSimpleStringCriterion',
                             u'ATSortCriterion',
                             u'ChangeSet',
                             u'Discussion Item',
                             u'Plone Site',
                             u'TempFolder',
                             u'ATCurrentAuthorCriterion',
                             u'ATPathCriterion',
                             u'ATRelativePathCriterion'),
     u'use_folder_contents': '',
     u'use_folder_tabs': (),
     u'verify_login_name': True,
     u'visible_ids': False,
     u'webstats_js': ''}

    """
    navtree_props = {}
    site_props = {}
    props_file = None
    try:
        if not xml_file:
            xml_file = os.path.join(os.path.dirname(__file__), 'xml_doctests', 'propertiestool.xml')
        props_file = open(xml_file)
        tools_properties = minidom.parse(props_file)
    except Exception, e:
        print "something wrong loading portal properties xml file"
    if props_file: props_file.close()

    objects = tools_properties.getElementsByTagName('object')
    for obj in objects :
        if obj.attributes['name'].nodeValue == 'navtree_properties':
            navtree_props = getProperties(obj)

        if obj.attributes['name'].nodeValue == 'site_properties':
            site_props = getProperties(obj)

    return (navtree_props, site_props)


if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)

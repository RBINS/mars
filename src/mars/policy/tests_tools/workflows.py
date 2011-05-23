import os.path
from xml.dom import minidom

def getWorkflows(xml_file='../profiles/default/workflows.xml'):
    """Get workflows_settings.

    >>> workflow_file = 'xml_doctests/workflows.xml'
    >>> workflows_settings = getWorkflows(xml_file=workflow_file)

    >>> workflows_settings['contents']
    [u'folder_workflow', u'intranet_folder_workflow', u'intranet_workflow', \
    u'mc_ploneboard_forum_workflow', u'one_state_workflow', u'plone_workflow',\
    u'ploneboard_comment_workflow', u'ploneboard_conversation_workflow',\
    u'ploneboard_forum_workflow', u'ploneboard_workflow',\
    u'simple_publication_workflow']

    >>> workflows_settings['default']
    u'simple_publication_workflow'

    >>> workflows_settings['bindings']
    {u'FormTextField': '', u'Ploneboard': u'ploneboard_workflow', \
    u'FormSelectionField': '', u'FormStringField': '', u'FormLinesField': '',\
    u'ATDateCriteria': '', u'ATPortalTypeCriterion': '', u'ATSortCriterion': '',\
    u'ATBooleanCriterion': '', u'FormPasswordField': '', u'FormFileField': '',\
    u'ATReferenceCriterion': '', u'FormMultiSelectionField': '',\
    u'FormCaptchaField': '', u'Plone Site': '', u'FieldsetFolder': '',\
    u'FormRichLabelField': '', u'ATSelectionCriterion': '',\
    u'FormFixedPointField': '', u'FormThanksPage': '',\
    u'PloneboardForum': u'mc_ploneboard_forum_workflow', u'Discussion Item': '',\
    u'FormBooleanField': '', u'ATCurrentAuthorCriterion': '',\
    u'ATDateRangeCriterion': '', u'FormSaveDataAdapter': '',\
    u'ATRelativePathCriterion': '', u'LinkInnerContentProxy': '',\
    u'PloneboardComment': u'ploneboard_comment_workflow',\
    u'ATSimpleStringCriterion': '', u'FileInnerContentProxy': '',\
    u'FormDateField': '', u'FormLikertField': '', u'FormIntegerField': '',\
    u'FormLabelField': '', u'FormMailerAdapter': '', u'ATSimpleIntCriterion': '',\
    u'ImageAttachment': '', u'InnerContentContainer': '',\
    u'ImageInnerContentProxy': '', u'FileAttachment': '',\
    u'PloneboardConversation': u'ploneboard_conversation_workflow',\
    u'Image': '', u'FormCustomScriptAdapter': '', u'ATListCriterion': '',\
    u'File': '', u'ATPathCriterion': '', u'PloneArticleTool': '',\
    u'FormRichTextField': ''}

    """

    wkf_props = {'contents': [], 'default': '', 'bindings': {}}
    props_file = None

    try:
        try:
            props_file = open(os.path.join(os.path.dirname(__file__), 'xml_doctests/', xml_file))
            workflows_settings = minidom.parse(props_file)
        except IOError:
            return wkf_props
    finally:
        if props_file:
            props_file.close()

    workflows = workflows_settings.getElementsByTagName('object')[1:]
    if workflows:
        for wf in workflows:
            attrs = wf.attributes
            name = attrs['name'].nodeValue
            wkf_props['contents'].append(name)

    bindings = workflows_settings.getElementsByTagName('bindings')
    if bindings:
        default = bindings[0].getElementsByTagName('default')
        if default:
            default_wf = default[0].getElementsByTagName('bound-workflow')[0]\
                        .attributes['workflow_id'].nodeValue
            wkf_props['default'] = default_wf

        types = bindings[0].getElementsByTagName('type')
        for _type in types:
            bound = _type.getElementsByTagName('bound-workflow')
            chain = ''
            if bound:
                chain = bound[0].attributes['workflow_id'].nodeValue

            wkf_props['bindings'][_type.attributes['type_id'].nodeValue] = chain

    return wkf_props

if __name__ == "__main__":
    import doctest
    OPTIONS = doctest.REPORT_ONLY_FIRST_FAILURE | doctest.ELLIPSIS |\
               doctest.NORMALIZE_WHITESPACE
    doctest.testmod(verbose=True, optionflags=OPTIONS)

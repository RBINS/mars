# -*- coding: utf-8 -*-
"""
Extensions install Product
"""
__author__ = "Jean-Philippe Camguilhem <jpc@makina-corpus.com>"

from StringIO import StringIO
from DateTime import DateTime
from Products.ExternalMethod.ExternalMethod import manage_addExternalMethod

from mars.tma.config import TMA_FOLDER, PROJECTNAME as PJNAME

form_template = """
<style type="text/css"><!-- @import url(../plone.css); --></style>
<div id="portal-logo"> <img src="../logo.jpg"/> </div>
<div id="portal-column-content">
<h1>Import %s from csvfile</h1>
  <form action="%s" method="post" enctype="multipart/form-data">
    <fieldset>
      <input type=file name="csv_%s"><br>
    </fieldset>
    <div align="center">
      <input type=submit value="Upload csv">
    </div>
  </form>
</div>
    """

config_checkers_template = """
<style type="text/css"><!-- @import url(../../plone.css); --></style>
<body>
<div id="portal-logo"> <img src="../../logo.jpg"/> </div>
<div id="portal-column-content">
  <h1>Portal Configuration checkers</h1>
      %s
      <hr/>
      <a href="run_all_tests"><h5>Run all tests</h5></a>
</div>
</body>
"""

run_all_tests_script = """
print  '<style type="text/css"><!-- @import url(../../plone.css); --></style>'
print '<body>'
print  '<div id="portal-logo"> <img src="../../logo.jpg"/> </div>'
print '<div id="portal-column-content">'
for external_method in container.objectValues(['External Method']):
    print context.restrictedTraverse(external_method.id)()
    print '<hr/>'
print '</div>'
print '</body>'
return printed
"""

def _getalltests(portal):
    """Return a list with all tests from config_checkers
    to provide external methods"""
    from mars.tma.Extensions import config_checkers
    return ((x.__name__, x.__doc__) for x in config_checkers.__dict__.values()
                                  if type(x).__name__ == 'function' and
                                  x.__name__.startswith('test'))

def install(portal, reinstall=False):
    """ External Method to install GENERIC_TMA """
    out = StringIO()
    print >> out, "Installation log of %s:" % PJNAME
    addScriptsFolder(portal)
    print >> out, "Zope Folder %s added" % TMA_FOLDER
    addFolderImportStructure(portal)
    print >> out, "Zope Folder import structure added"
    addFolderImportUsersAndGroups(portal)
    print >> out, "Zope Folder import users added"
    addFolderConfigCheckers(portal)
    print >> out, "Zope Folder Config Checkers added"
    return out.getvalue()

def uninstall(portal, reinstall=False):
    """Uninstall product."""
    out = StringIO()
    print >> out, "Zope Folder %s deleted" % TMA_FOLDER
    removeMC_SCRIPTS(portal)
    return out.getvalue()

def addScriptsFolder(portal):
    """ Add a Zope Folder to store external methods for tma"""
    scripts_folder = getattr(portal, TMA_FOLDER, None)
    if scripts_folder is None:
        portal.manage_addProduct['OFSP'].manage_addFolder(TMA_FOLDER)
        scripts_folder = getattr(portal, TMA_FOLDER, None)
        # unacquire view permission and puti for any role
        # only zope administartor can view in this folder
        scripts_folder.manage_permission('View',('Manager',),acquire=0)

def addFolderImportStructure(portal):
    """ Add a Zope Folder to store import structure stuff"""
    scripts_folder = getattr(portal, TMA_FOLDER, None)
    scripts_folder.manage_addProduct['OFSP'].manage_addFolder('import_structure')
    import_structure_folder = getattr(scripts_folder, 'import_structure', None)

    # add external method for import structure
    import_structure_folder.manage_addProduct[
            'ExternalMethod'].manage_addExternalMethod('structure_from_csv',
                                                  'Import struture/content'
                                                  'from csvfile',
                                                   PJNAME + '.csv_imports',
                                                   'structure_from_csv')
    # add dtml_document to provide form
    import_structure_folder.manage_addProduct[
        'OFSP'].manage_addDTMLDocument('index_html',
                                       'CSV Upload Form',
                                       form_template % ('structure/content',
                                                        'structure_from_csv',
                                                        'structure'
                                                        )
                                      )

def addFolderImportUsersAndGroups(portal):
    """ Add a Zope Folder to store import structure stuff"""
    scripts_folder = getattr(portal, TMA_FOLDER, None)
    scripts_folder.manage_addProduct['OFSP'].manage_addFolder('import_users')
    import_users_folder = getattr(scripts_folder, 'import_users', None)

    # add external method for import structure
    import_users_folder.manage_addProduct[
            'ExternalMethod'].manage_addExternalMethod('users_from_csv',
                                                  'Import users and groups'
                                                  'from csvfile',
                                                   PJNAME + '.csv_imports',
                                                   'users_from_csv')
    # add dtml_document to provide form
    import_users_folder.manage_addProduct[
        'OFSP'].manage_addDTMLDocument('index_html',
                                       'CSV Upload Form',
                                       form_template % ('users and groups',
                                                        'users_from_csv',
                                                        'users'
                                                        )
                                      )

def addFolderConfigCheckers(portal):
    """ Add a Zope Folder to store import structure stuff"""
    scripts_folder = getattr(portal, TMA_FOLDER, None)
    scripts_folder.manage_addProduct['OFSP'].manage_addFolder('config_checkers')
    config_checkers_folder = getattr(scripts_folder, 'config_checkers', None)

    tests_links = ''

    for test in _getalltests(portal):
        config_checkers_folder.manage_addProduct['ExternalMethod'].\
                               manage_addExternalMethod(test[0],
                                                        test[1],
                                                        PJNAME + \
                                                        '.config_checkers',
                                                        test[0])
        tests_links += '<p><a href="%s">%s</a></p>' % (test)

    # add dtml_document to provide form
    config_checkers_folder.manage_addProduct[
        'OFSP'].manage_addDTMLDocument('index_html',
                                       'Config checkers',
                                       config_checkers_template % tests_links
                                      )

    # add python script run_all_tests
    config_checkers_folder.manage_addProduct[
        'PythonScripts'].manage_addPythonScript('run_all_tests')
    script = getattr(config_checkers_folder, 'run_all_tests').\
            ZPythonScript_edit(params='',body=run_all_tests_script)

def removeMC_SCRIPTS(portal):
    """Uninstall TMA_FOLDER."""
    scripts_folder = getattr(portal, TMA_FOLDER, None)
    if scripts_folder is not None:
        portal.manage_delObjects(TMA_FOLDER)


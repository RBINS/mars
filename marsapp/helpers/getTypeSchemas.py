# Python imports
from StringIO import StringIO
import os
import zipfile
import tempfile

# Zope imports
from Acquisition import aq_base

# CMF/Plone/Archetypes imports
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import OrderedDict
from Products.Archetypes.utils import capitalize
#from Products.generator import i18n

from Products.ATContentTypes.content.document import ATDocument
from marsapp.content.analysis import MarsAnalysis, MarsAnalysisAbsoluteDating, MarsAnalysisRelativeDating
from marsapp.content.artefact import MarsArtefact, MarsArtefactIndividual, MarsArtefactAssemblage
from marsapp.content.collection import MarsCollection
from marsapp.content.curation import MarsCuration
from marsapp.content.excavation import MarsExcavation
from marsapp.content.fauna import MarsFaunaRemain, MarsFaunaIndividual, MarsFaunaAssemblage, MarsFaunaReferenceSample
from marsapp.content.flora import MarsFloraRemain, MarsFloraIndividual, MarsFloraAssemblage, MarsFloraReferenceSample
from marsapp.content.hominid import MarsHominidRemain, MarsHominidIndividual, MarsHominidAssemblage, MarsHominidReferenceSample
from marsapp.content.institution import MarsInstitution
from marsapp.content.people import MarsPeople
from marsapp.content.site import MarsSite
from marsapp.content.stratigraphy import MarsStratigraphy, MarsStratigraphicalLayer
from marsapp.content.structure import MarsStructureAssemblage
#from marsapp.content.externalfile import MarsExternalFile
#from marsapp.content.multimedia
#import picture

CLASSES = (
    ATDocument,
    MarsPeople,
    MarsInstitution,
    MarsCuration,
    MarsSite,
    MarsExcavation,
    MarsStratigraphy, MarsStratigraphicalLayer,
    MarsCollection,
    MarsArtefact, MarsArtefactIndividual, MarsArtefactAssemblage,
    MarsFaunaRemain, MarsFaunaIndividual, MarsFaunaAssemblage, MarsFaunaReferenceSample,
    MarsFloraRemain, MarsFloraIndividual, MarsFloraAssemblage, MarsFloraReferenceSample,
    MarsHominidRemain, MarsHominidIndividual, MarsHominidAssemblage, MarsHominidReferenceSample,
    MarsStructureAssemblage,
    MarsAnalysis, MarsAnalysisAbsoluteDating, MarsAnalysisRelativeDating,
#    from marsapp.content.externalfile import MarsExternalFile
#    from marsapp.content.multimedia
#    import picture
    )

RESPONSE_BLOCK_SIZE = 32768

ARCHIVE_NAME = 'mars_documentation'
ARCHIVE_FILE = ARCHIVE_NAME + '.zip'

READMEFILE = """Le dossier contient une série de fichiers dont le nom se termine par '-README.txt'.

Chaque fichier présente les données importantes pour un type de contenu du système MARS.

signification des valeurs présentées dans chaque fichier:

- Archetype_name: nom 'human readable'

- All schemata: liste des pages que consituent le formulaire d'édition du contenu.

Puis pour chaque schemata (page d'édition), chaque champ est listé avec ses principales caractéristiques:

- field type: type de champs
    par exemple: integer (entier), boolean (vrai/faux), string (ligne de
    texte), text (texte multiligne), lines (liste d'éléments), file (fichier),
    reference (lien entre deux objets), marscat (catégorie mars).

- required: champ obligatoire, doit contenir une valeur

- Multivalued: champ qui peut contenir plus d'une valeur

- Searchable: champ indexé dans l'index général SearchableText, que l'on peut
  intérrogé par le quick search.

- widget: types d'interface utilisées pour la vue et l'édition du champs.

- index: type d'index utilisé dans le catalogue pour ce champs spécifique.

- index priority: Priorité à l'indexation du champs (0=faible, 5=la plus
  haute). Valeur à remplir par les utilisateurs.
"""

def printout(out, s):
    try:
        print >> out, s.encode('utf-8')
    except (TypeError, UnicodeDecodeError, ValueError):
        pass

def createTempZipFile(self):
    """
    Create a temporary ZipFile on the file system
    Returns the path of temporary file
    Inspired from PloneFilesZip by Ingeniweb
    """
    out = StringIO()

#    portal_url = getToolByName(self, 'portal_url')
#    portal = portal_url.getPortalObject()
#    mimetypes_registry = getToolByName(portal, 'mimetypes_registry')

    # Create temporary file
    fd, path = tempfile.mkstemp('.zippe')
    os.close(fd)

    # out_file = tempfile.TemporaryFile(suffix='.zippe')
    zip = zipfile.ZipFile(path, 'w', zipfile.ZIP_DEFLATED)

#    portal = self.portal_url.getPortalObject()
#    ttool = portal.portal_types
#    portal.invokeFactory('Folder', id='TempTestFolder')
#    tmpfolder = getattr(portal, 'TempTestFolder')

#    printout(out, tmpfolder.getId())

#    portal.manage_delObjects(['TempTestFolder'])
#    printout(out, hasattr(portal, 'TempTestFolder'))

#    mymodule = __import__('Products.MarsFramework.content.multimedia')

#    print mymodule

#    zip.writestr('output.txt', out.getvalue())

    for imported_class in CLASSES:
        file_path = '%s/%s-README.txt' % ( ARCHIVE_NAME,
                                           imported_class.__name__ )
        textfile = outputContentFile(self, imported_class)
        zip.writestr(file_path, textfile)
    
    zip.writestr( '%s/README.txt' %ARCHIVE_NAME, READMEFILE)

    zip.close()
    return path


def downloadZipDoc(self, archive_name=ARCHIVE_FILE):

    zip_path = createTempZipFile(self)

    RESPONSE = self.REQUEST.RESPONSE
    RESPONSE.setHeader('Content-Type','application/download')
    RESPONSE.setHeader('Content-Disposition',
                       'attachment; filename=%s' % archive_name)
    RESPONSE.setHeader('content-length', str(os.stat(zip_path)[6]))

    # If using the filestream_iterator, it wouldn't be possible to delete the
    # out_filename later.
    # So... emulating ZPublisher.Iterators.filestream_iterator
    fp = open(zip_path, 'rb')
    while True:
        data = fp.read(RESPONSE_BLOCK_SIZE)
        if data:
            RESPONSE.write(data)
        else:
            break
    fp.close()
    os.remove(zip_path)
    return


def getSchemas(self):
    out = StringIO()

#    typesTool = getattr(ploneroot, 'portal_types')

#    for TypeInfo in typesTool.listTypeInfo():
#        if TypeInfo.product == 'MarsFramework':
#            printout(out, TypeInfo.getId())
#            printout(out, TypeInfo.title)
#            printout(out, TypeInfo.description)
#            printout(out, TypeInfo.__dict__)


    for imported_class in CLASSES:
        textfile = outputContentFile(self, imported_class)
        printout(out, textfile)

    return out.getvalue()

def outputContentFile(self, imported_class):
    out = StringIO()
    trans = getToolByName(self, 'translation_service', None)
    utranslate = trans.utranslate
    obj = imported_class("object_id")

    values = dict()

    values['meta_type'] = obj.meta_type
    values['archetype_name'] = obj.archetype_name

    printout(out, obj.meta_type)
    printout(out, '')
    printout(out, '  archetype_name: ' + obj.meta_type)
    printout(out, '')
    schemata_names = obj.schema.getSchemataNames()
    exclude_schemata = ('metadata',)
    schemata_names = [s for s in schemata_names if s not in exclude_schemata]
    printout(out, '')
    printout(out, '  All schemata (except metadata):')
    printout(out, '    %s' % ', '.join(schemata_names))
#    for schemata_name in schemata_names:
#        printout(out, '    %s' %schemata_name)
    printout(out, '')
    for schemata_name in schemata_names:
        printout(out, '    schemata: %s' %schemata_name)
        printout(out, '')
        for field in obj.Schema().filterFields(schemata=schemata_name):
            printout(out, '      field: %s' %field.__name__)
            printout(out, '')
            printout(out, '        field type: %s' %field.type)
            printout(out, '        required: %s' %bool(field.required))
            if field.default:
                printout(out, '        default: %s' %str(field.default))
            if field.default_method is not None:
                printout(out, '        default_method: %s' \
                                                    %field.default_method)
            if field.vocabulary is not ():
                printout(out, '        vocabulary: %s' %str(field.vocabulary))
            if field.enforceVocabulary:
                printout(out, '        enforceVocabulary: %s' \
                                                %bool(field.enforceVocabulary))
            printout(out, '        Multivalued: %s' %bool(field.required))
            printout(out, '        Searchable: %s' %bool(field.required))
            if field.isMetadata:
                printout(out, '        isMetadata: %s' %bool(field.isMetadata))

            capName = capitalize(field.getName())
            if field.accessor != 'get'+capName:
                printout(out, '        accessor: %s' %field.accessor)
            if field.edit_accessor != 'getRaw'+capName:
                printout(out, '        edit_accessor: %s' %field.edit_accessor)
            if field.mutator != 'set'+capName:
                printout(out, '        mutator: %s' %field.mutator)
            if field.mode != 'rw':
                printout(out, '        mode: %s' %field.mode)

            if field.read_permission != 'View':
                printout(out, '        read_permission: %s' \
                                                        %field.read_permission)
            if field.write_permission != 'Modify portal content':
                printout(out, '        write_permission: %s' \
                                                    %field.write_permission)

#            printout(out, '        storage: %s' %field.storage.getName())

#            printout(out, '        generateMode: %s' %field.generateMode)
#            printout(out, '        force: %s' %field.force)

            printout(out, '        widget: %s' %field.widget.getName())
            printout(out, '          widget label: %s' %field.widget.label)
#            if hasattr(field.widget, 'domain'):
#                domain = field.widget.domain
#            else:
#                domain = 'plone'
#            if hasattr(field.widget, 'label_msgid'):
#                printout(out, '          widget label msg_id: %s' \
#                                                    %field.widget.label_msgid)
#                printout(out, '          widget label (fr): %s' \
#                            %utranslate(domain,
#                                        field.widget.label_msgid,
#                                        target_language='fr'))
            if field.widget.description:
                printout(out, '          widget description: %s' \
                                                    %field.widget.description)

#            printout(out, '        validators: %s' %str(field.validators))

            printout(out, '        index: %s' %field.index)
            if field.index_method != '_at_accessor':
                printout(out, '        index_method: %s' %field.index_method)

#            printout(out, '        languageIndependent: %s' %field.languageIndependent)
            printout(out, '')
            printout(out, '        index priority: ')
            printout(out, '')


    return out.getvalue()



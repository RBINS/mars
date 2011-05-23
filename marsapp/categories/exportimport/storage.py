from persistent.dict import PersistentDict
from zope.component import getUtility, queryUtility, queryMultiAdapter

from marsapp.categories.storage import IMarscatsSettingsStorage

from Products.GenericSetup.interfaces import IBody
from Products.GenericSetup.utils import XMLAdapterBase

def importMarscatsSettingsStorage(context):
    """Import marscats settings."""
    logger = context.getLogger('marsapp.categories')

    body = context.readDataFile('marscats.xml')
    if body is None:
        logger.info("Nothing to import")
        return

    storage = getUtility(IMarscatsSettingsStorage)

    importer = queryMultiAdapter((storage, context), IBody)
    if importer is None:
        logger.warning("Import adapter missing.")
        return

    importer.body = body
    logger.info("Imported.")

def exportMarscatsSettingsStorage(context):
    """Export marscats settings."""
    logger = context.getLogger('marsapp.categories')

    storage = queryUtility(IMarscatsSettingsStorage)

    if storage is None:
        logger.info("Nothing to export")
        return

    exporter = queryMultiAdapter((storage, context), IBody)
    if exporter is None:
        logger.warning("Export adapter missing.")
        return

    context.writeDataFile('marscats.xml', exporter.body, exporter.mime_type)
    logger.info("Exported.")


class MarscatsSettingsStorageNodeAdapter(XMLAdapterBase):
    __used_for__ = IMarscatsSettingsStorage

    def _exportNode(self):
        """
        Export the object as a DOM node.
        """
        output = self._doc.createElement('object')
        storage = self.context._fields
        for field in storage:
            node = self._doc.createElement('field')
            node.setAttribute('name', field)
            if storage[field].has_key('startup_directory'):
                node.setAttribute('startup_directory',
                              storage[field].get('startup_directory'))
            portal_types = storage[field].get('portal_types')
            if portal_types is not None:
                typesnode = self._doc.createElement('portal_types')
                for portal_type in portal_types:
                    child = self._doc.createElement('portal_type')
                    child.setAttribute('name', portal_type)
                    startupdir = portal_types.get(portal_type)
                    if startupdir:
                        child.setAttribute('startup_directory', startupdir)
                    typesnode.appendChild(child)
                node.appendChild(typesnode)
            output.appendChild(node)
        return output

    def _importNode(self, node):
        """
        Import the object from the DOM node.
        """
        storage = self.context
        purge = self.environ.shouldPurge()
        if node.getAttribute('purge'):
            purge = self._convertToBoolean(node.getAttribute('purge'))
        if purge:
            self._purgeMarscatsSettings()
        for child in node.childNodes:
            nodename = child.nodeName
            if nodename != 'field':
                continue
            fieldname = child.getAttribute('name')
            if child.getAttribute('purge'):
                purge = self._convertToBoolean(child.getAttribute('purge'))
                if purge:
                     self._purgeFieldSettings(fieldname)
            dsd = child.getAttribute('startup_directory')
            if dsd:
                storage.setStartupDir(fieldname, dsd)
            for grandchild in child.childNodes:
                grandchildname = grandchild.nodeName
                if grandchildname != 'portal_types':
                    continue
                if grandchild.getAttribute('purge'):
                    purge = self._convertToBoolean(
                                        grandchild.getAttribute('purge'))
                    if purge:
                        self._purgeTypesSettings(fieldname)
                for tchild in grandchild.childNodes:
                    nodename = tchild.nodeName
                    if nodename != 'portal_type':
                        continue
                    portal_type = tchild.getAttribute('name')
                    sd = tchild.getAttribute('startup_directory')
                    if sd is None: sd = ''
                    storage.setStartupDir(fieldname, sd, portal_type)

    def _purgeMarscatsSettings(self):
        self.context._fields.clear()

    def _purgeFieldSettings(self, fieldname):
        if fieldname in self.context._fields:
            self.context._fields[fieldname].clear()

    def _purgeTypesSettings(self, fieldname):
        if fieldname in self.context._fields:
            field = self.context._fields[fieldname]
            if 'portal_types' in field:
                field['portal_types'].clear()

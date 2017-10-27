#-*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes import PloneMessageFactory as _
from Products.Archetypes import config
from Products.Archetypes.Field import ReferenceField
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerPropertyType
from Products.Archetypes.public import DisplayList
from Products.CMFCore.utils import getToolByName
from container import MarsCategoriesContainer
from storage import IMarscatsSettingsStorage
from widget import MarscatWidget
from zope.component import getUtility
from zope.interface import implements
from .interfaces import IMarsCatField


def getTitledPath(obj, startup_folder_url, path=None):
    if path is None:
        path = []
    if not isinstance(obj, MarsCategoriesContainer):
        path.insert(0, obj.Title())
        path = getTitledPath(obj.aq_inner.aq_parent, startup_folder_url, path)
    return path

class MarscatField(ReferenceField):
    """ Mars Categories System Field
    """
    implements(IMarsCatField)
    def __init__(self, *args, **kwargs):
        if not kwargs['relationship']:
            kwargs['relationship'] = 'hasMarsCat%s' % args[0]
        ReferenceField.__init__(self, *args, **kwargs)

    _properties = ReferenceField._properties.copy()
    _properties.update({
        'type' : 'marscat',
        'default': None,
        'widget': MarscatWidget,
        'allowed_types': ('Mars Category',),
        'multiValued': True,
        #'allowed_type_column' : 'portal_type',
        #'addable': 1,
        #'destination': None,
        #'relationship': None,
        #'categories': (),
        #'index_method' : '_at_edit_accessor',
        })

    security  = ClassSecurityInfo()
    def _Vocabulary(self, content_instance):
        """overload
            Archetypes Products.Archetypes.Field.ReferenceField._Vocabulary to make a restriction on the _path_ for performance gain
            """
        pairs = []
        pc = getToolByName(content_instance, 'portal_catalog')
        uc = getToolByName(content_instance, config.UID_CATALOG)
        purl = getToolByName(content_instance, 'portal_url')

        allowed_types = self.allowed_types
        allowed_types_method = getattr(self, 'allowed_types_method', None)
        if allowed_types_method:
            meth = getattr(content_instance,allowed_types_method)
            allowed_types = meth(self)

        skw = allowed_types and {'portal_type':allowed_types} or {}
        brains = uc.searchResults(skw)

        if self.vocabulary_custom_label is not None:
            label = lambda b:eval(self.vocabulary_custom_label, {'b': b})
        elif self.vocabulary_display_path_bound != -1 and len(brains) > self.vocabulary_display_path_bound:
            at = _(u'label_at', default=u'at')
            label = lambda b:u'%s %s %s' % (self._brains_title_or_id(b, content_instance),
                                             at, b.getPath())
        else:
            label = lambda b:self._brains_title_or_id(b, content_instance)

        # The UID catalog is the correct catalog to pull this
        # information from, however the workflow and perms are not accounted
        # for there. We thus check each object in the portal catalog
        # to ensure it validity for this user.
        portal_base = purl.getPortalPath()
        path_offset = len(portal_base) + 1

        abs_paths = {}
        abs_path = lambda b, p=portal_base: '%s/%s' % (p, b.getPath())

        # modifications
        sd =  (portal_base +
               "/" +
               self.widget.getStartupDirectory(
                   content_instance, self)).replace('//', '/')

        for b in brains:
            apath = abs_path(b)
            if apath.startswith(sd):
                abs_paths.update({apath:b})
        # end modifications

        pc_brains = pc(path=abs_paths.keys(), **skw)

        for b in pc_brains:
            b_path = b.getPath()
            # translate abs path to rel path since uid_cat stores
            # paths relative now
            path = b_path[path_offset:]
            # The reference field will not expose Refrerences by
            # default, this is a complex use-case and makes things too hard to
            # understand for normal users. Because of reference class
            # we don't know portal type but we can look for the annotation key in
            # the path
            if self.referenceReferences is False and \
               path.find(config.REFERENCE_ANNOTATION) != -1:
                continue

            # now check if the results from the pc is the same as in uc.
            # so we verify that b is a result that was also returned by uc,
            # hence the check in abs_paths.
            if abs_paths.has_key(b_path):
                uid = abs_paths[b_path].UID
                if uid is None:
                    # the brain doesn't have an uid because the catalog has a
                    # staled object. THAT IS BAD!
                    raise ReferenceException("Brain for the object at %s "\
                        "doesn't have an UID assigned with. Please update your"\
                        " reference catalog!" % b_path)
                pairs.append((uid, label(b)))

        if not self.required and not self.multiValued:
            no_reference = _(u'label_no_reference',
                             default=u'<no reference>')
            pairs.insert(0, ('', no_reference))

        __traceback_info__ = (content_instance, self.getName(), pairs)

        return DisplayList(pairs)

    def getStartupDirectory(self, instance):
        storage = getUtility(IMarscatsSettingsStorage)
        portal_type = instance.portal_type
        name = self.getName()
        return storage.getStartupDir(name, portal_type, ispath=True)

    def get(self, instance, **kwargs):
        startup_directory = self.getStartupDirectory(instance)
        portal_url = getToolByName(instance, 'portal_url')
        portal = portal_url.getPortalObject()
        startup_folder = portal.restrictedTraverse(str(startup_directory))
        startup_folder_url = startup_folder.absolute_url()
        refcat = getToolByName(instance, 'reference_catalog')
        items = []
        kwargs['aslist'] = True
        value = ReferenceField.getRaw(self, instance,  **kwargs)
        for uid in value:
            obj = refcat.lookupObject(uid)
            item = getTitledPath(obj, startup_folder_url)
            items.append(' / '.join(item))
        return items

registerField(MarscatField, title='Mars Categories',
              description=('Used for categorizing MARS Collection Objects.'))

registerPropertyType('categories', 'tuple', MarscatField)

import zope.interface
from collective.z3cform.widgets.token_input_widget import TokenInputWidget
from marsapp.content.widgets.interfaces import IKeywordWidget
from plone import api
from z3c.form import widget
from z3c.form.interfaces import IFieldWidget, NO_VALUE
from zope.browserpage import ViewPageTemplateFile


class KeywordWidget(TokenInputWidget):
    zope.interface.implementsOnly(IKeywordWidget)
    input_template = ViewPageTemplateFile('keyword_input.pt')

    def allowed_to_add_keyword(self):
        """
        :return:
        """
        portal_properties = api.portal.get_tool('portal_properties')
        add_keyword_roles = portal_properties.site_properties.allowRolesToAddKeywords
        if not add_keyword_roles:
            return True
        else:
            return bool(set(add_keyword_roles).intersection(api.user.get_roles()))

    def extract(self, default=NO_VALUE):
        """See z3c.form.interfaces.IWidget."""
        request = self.request
        name = self.name.replace('.', '-')  # ':list' doesn't work with dotted field names
        existing_keywords_name = name + '_existing_keywords'
        keywords_name = name + '_keywords'
        if existing_keywords_name not in request and keywords_name not in request:
            return default

        existing_keywords = (n.strip() for n in request.get(existing_keywords_name, default or ()) if n.strip())
        keywords = (n.strip() for n in request.get(keywords_name, default or ()) if n.strip())
        return "\n".join((sorted(set(existing_keywords).union(keywords))))

    def update(self):
        super(KeywordWidget, self).update()
        if isinstance(self.value, basestring):
            self.value = self.value.split('\n')


@zope.interface.implementer(IFieldWidget)
def KeywordFieldWidget(field, request):
    """IFieldWidget factory for KeywordFieldWidget."""
    return widget.FieldWidget(field, KeywordWidget(request))

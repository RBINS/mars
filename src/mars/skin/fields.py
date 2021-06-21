
import zope.component
import zope.interface
import zope.schema.interfaces
from zope import schema

import plone.supermodel.exportimport
from plone.schemaeditor.fields import FieldFactory
from plone.formwidget.contenttree import UUIDSourceBinder
from z3c.form import interfaces
from z3c.form.widget import Widget, FieldWidget
from z3c.form.browser import widget
from z3c.relationfield.schema import RelationChoice, RelationList


URLFactory = FieldFactory(
    schema.URI, u'URL')


class IURLWidget(interfaces.IWidget):
    """URL widget."""


@zope.interface.implementer_only(IURLWidget)
class URLWidget(widget.HTMLTextInputWidget, Widget):
    """Input type url widget implementation."""

    klass = u'url-widget'
    css = u'text'
    value = u''

    def update(self):
        super(URLWidget, self).update()
        widget.addFieldClass(self)


@zope.component.adapter(zope.schema.interfaces.IField, interfaces.IFormLayer)
@zope.interface.implementer(interfaces.IFieldWidget)
def URLFieldWidget(field, request):
    """IFieldWidget factory for URLWidget."""
    return FieldWidget(field, URLWidget(request))


RelationListFactory = FieldFactory(RelationList, u'Relations', value_type=RelationChoice(source=UUIDSourceBinder()))

RelationListHandler = plone.supermodel.exportimport.BaseHandler(RelationList)
RelationChoiceHandler = plone.supermodel.exportimport.ChoiceHandler(RelationChoice)

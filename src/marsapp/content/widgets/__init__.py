# -*- coding: utf-8 -*-
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.autoform.interfaces import WIDGETS_KEY
from collective.z3cform.widgets import _directives_values


widget = 'marsapp.content.widgets.keyword_widget.KeywordFieldWidget'

if _directives_values:
    # groked form
    # _directives_values.setdefault(WIDGETS_KEY, {})
    _directives_values[WIDGETS_KEY]['subjects'] = widget
else:
    # plone 4.3 not groked form
    _widget_values = ICategorization.queryTaggedValue(WIDGETS_KEY, {})
    _widget_values['subjects'] = widget
    ICategorization.setTaggedValue(WIDGETS_KEY, _widget_values)


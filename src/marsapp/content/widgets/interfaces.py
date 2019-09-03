from z3c.form.interfaces import ITextLinesWidget


class IKeywordWidget(ITextLinesWidget):
    """Text lines widget."""

    def allowed_to_add_keyword(self):
        """"""

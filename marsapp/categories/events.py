def modifiedCategoryEventHandler(ob, event):
    """A MARS Category was modified."""
    for bref in ob.getBRefs():
        bref.reindexObject()


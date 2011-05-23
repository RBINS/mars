GLOBALS = globals()

from permissions import DEFAULT_ADD_CONTENT_PERMISSION as \
                                            ADD_CONTENT_PERMISSION

def initialize(context):
    from Products.CMFCore.utils import ContentInit
    import category, container
    from Products.Archetypes.public import process_types, listTypes
    content_types, constructors, ftis = process_types(
        listTypes('marsapp.categories'), 'marsapp.categories')
    ContentInit('marsapp.categories Content',
                content_types      = content_types,
                permission         = ADD_CONTENT_PERMISSION,
                extra_constructors = constructors,
                fti                = ftis,
                ).initialize( context )

#    from Products.CMFCore.utils import ToolInit
#    import tool
#    tools = (tool.MarsCategoriesTool,)
#    ToolInit('Mars Categories Tool',
#             tools=tools,
#             icon='tool_icon.gif'
#             ).initialize( context )

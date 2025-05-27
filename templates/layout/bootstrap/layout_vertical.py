from django.template.loader import render_to_string
from web_project.template_helpers.theme import TemplateHelper

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in web_project/__init__.py
"""


class TemplateBootstrapLayoutVertical:
    def __init__(self):
        self.template_name = 'layout/vertical.html'
    
    def render(self, request, context=None):
        if context is None:
            context = {}
        return render_to_string(self.template_name, context, request=request)

    def init(context):
        context.update(
            {
                "layout": "vertical",
                "content_navbar": True,
                "content_layout": "compact",
                "is_navbar": True,
                "is_menu": True,
                "is_footer": True,
            }
        )

        # map_context according to updated context values
        TemplateHelper.map_context(context)



        return context

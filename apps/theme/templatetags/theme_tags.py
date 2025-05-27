from django import template

register = template.Library()

@register.inclusion_tag('theme/variables.html')
def get_theme_variables():
    return {
        'theme': 'light',
        'layout': 'vertical',
        'style': 'default',
        'rtl': False,
        'skin': 'default',
        'navbar_type': 'fixed',
        'footer_type': 'static',
    }

@register.simple_tag
def get_theme_config():
    return {
        'layout_path': 'layout/bootstrap/layout_vertical.html',
        'assets_path': '/static/assets/',
    }
